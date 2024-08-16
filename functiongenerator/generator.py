import json
import os
import re
import subprocess
import sys
import time

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from templates import Templates
from constants import (
    NUM_FUNCTIONS,
    PATH_LOG_FILE,
    PATH_JSON_FILE,
    DIR_RESULTS,
    DIR_C_FILES,
    DIR_LLM_RESPONSES,
    LLMModel,
)
from utils.llm import LLMClientFactory
from utils.utils import get_printf_format

load_dotenv()
# api_key = os.environ.get("TOGETHER_API_KEY")
# client = LLMClientFactory.create_client(LLMModel.TOGETHER_AI, api_key=api_key)

api_key = os.environ.get("OPENAI_API_KEY")
client = LLMClientFactory.create_client(LLMModel.OPEN_AI, api_key=api_key)

os.makedirs(DIR_RESULTS, exist_ok=True)
os.makedirs(DIR_C_FILES, exist_ok=True)
os.makedirs(DIR_LLM_RESPONSES, exist_ok=True)

# Load existing JSON file or initialize a new one
if os.path.exists(PATH_JSON_FILE):
    with open(PATH_JSON_FILE, "r") as outfile:
        code_snippets = json.load(outfile)
    valid_snippet_count = len(code_snippets)
else:
    valid_snippet_count = 0
    with open(PATH_JSON_FILE, "w") as outfile:
        json.dump([], outfile, indent=4)

code_snippets = []

# Initialize the start time for the first function
previous_time = time.time()

while valid_snippet_count < NUM_FUNCTIONS:
    generation_query = Templates.format("Generate")
    response = client.create_chat_completion([generation_query])

    generation_res = response.choices[0].message.content
    pattern = r"```(?:C)?(.*?)```"
    match = re.search(pattern, generation_res, re.DOTALL)

    print("generation response:" + generation_res)

    if match:
        code_snippet = match.group(1).strip()
        if "scanf" in code_snippet or "printf" in code_snippet:
            continue

        c_file_name = f"{valid_snippet_count + 1:05d}.c"
        c_file_path = os.path.join(DIR_C_FILES, c_file_name)

        with open(c_file_path, "w") as f:
            f.write(code_snippet)
            f.write("\n\n")
            f.write("#include <stdio.h>\n")
            f.write("int main() {\n")
            f.write("    return 0;\n")
            f.write("}\n")

        # Use gcc to compile the code to check whether it is compilable
        compile_result = subprocess.run(
            ["gcc", "-o", "temp_code", c_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if compile_result.returncode == 0:
            run_result = subprocess.run(
                ["./temp_code"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            input_query = Templates.format("Input")
            response = client.create_chat_completion(
                [generation_query, generation_res, input_query]
            )
            input_res = response.choices[0].message.content

            print("input response:" + input_res)

            pattern = r"\[.*?\]"
            matches = re.findall(pattern, input_res)
            if matches:
                io_pairs = []
                for match in matches:
                    function_signature = re.search(
                        r"(unsigned\s+)?(int|float|double|char|short|long\s+long|long|int8_t|uint8_t|int16_t|uint16_t|int32_t|uint32_t|int64_t|uint64_t|size_t|ptrdiff_t)\s+(\w+)\s*\((.*?)\)",
                        code_snippet,
                    )

                    if function_signature:
                        return_type = function_signature.group(2)
                        function_name = function_signature.group(3)
                        parameter_list = function_signature.group(4)

                        parameter_types = (
                            [
                                param.strip().split(" ")[0]
                                for param in parameter_list.split(",")
                            ]
                            if parameter_list
                            else []
                        )

                        try:
                            cleaned_input = json.loads(match)
                            str_cleaned_input = [str(i) for i in cleaned_input]
                        except json.JSONDecodeError:
                            print(f"Failed to decode input: {match}")
                            continue

                        with open(c_file_path, "w") as f:
                            f.write(code_snippet)
                            f.write("\n\n")
                            f.write("#include <stdio.h>\n")
                            f.write("int main() {\n")
                            # Join the inputs as a string
                            inputs = ", ".join(str_cleaned_input)
                            format_string = get_printf_format(return_type)
                            f.write(
                                f'    printf("{format_string}\\n", {function_name}({inputs}));\n'
                            )
                            f.write("    return 0;\n")
                            f.write("}\n")

                        # Use undefined behavior sanitizer to check for UB
                        compile_result = subprocess.run(
                            [
                                "gcc",
                                "-fsanitize=undefined",
                                "-fsanitize=address",
                                "-o",
                                "temp_code",
                                c_file_path,
                            ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )

                        if compile_result.returncode == 0:
                            try:
                                run_result = subprocess.run(
                                    ["./temp_code"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    timeout=5,
                                )
                                runtime_errors = run_result.stderr.decode()
                                if not (
                                    "runtime error" in runtime_errors
                                    or "undefined behavior" in runtime_errors
                                    or "Undefined behavior" in runtime_errors
                                    or "AddressSanitizer" in runtime_errors
                                    or "SEGV" in runtime_errors
                                ):
                                    io_pairs.append(
                                        [
                                            str_cleaned_input,
                                            run_result.stdout.decode().strip(),
                                        ]
                                    )
                                else:
                                    print(f"Runtime error for input '{match}'")
                                    continue
                            except subprocess.TimeoutExpired:
                                print(
                                    f"Execution timed out for '{c_file_name}'. The process was terminated."
                                )
                                continue
                        else:
                            print(
                                f"Compile error for input '{match}':\n{compile_result.stderr.decode()}"
                            )
                if len(io_pairs) > 0:
                    print(io_pairs)
                    print(len(io_pairs))
                    snippet_data = {
                        "function_name": function_name,
                        "parameter_types": parameter_types,
                        "return_type": return_type,
                        "function": code_snippet,
                        "io_list": io_pairs,
                    }
                    code_snippets.append(snippet_data)

                    # Delete and replace the .c file without the main function
                    os.remove(c_file_path)
                    with open(c_file_path, "w") as f:
                        f.write(code_snippet)

                    valid_snippet_count += 1

                    current_time = time.time()
                    time_interval = current_time - previous_time
                    previous_time = current_time
                    log_entry = f"func{valid_snippet_count}: {time_interval} s"
                    with open(PATH_LOG_FILE, "a") as log_file:
                        log_file.write(log_entry + "\n")

                    with open(PATH_JSON_FILE, "r+") as outfile:
                        data = json.load(outfile)
                        data.append(snippet_data)
                        outfile.seek(0)
                        json.dump(data, outfile, indent=4)

                    # Save the LLM response and input to a file
                    llm_response_path = os.path.join(
                        DIR_LLM_RESPONSES, f"{c_file_name}_llm_response.txt"
                    )
                    with open(llm_response_path, "w") as llm_file:
                        llm_file.write("User Input (First Request):\n")
                        llm_file.write(generation_query + "\n\n")
                        llm_file.write("LLM Response (First Response):\n")
                        llm_file.write(generation_res + "\n\n")
                        llm_file.write("User Input (Second Request):\n")
                        llm_file.write(input_query + "\n\n")
                        llm_file.write("LLM Response (Second Response):\n")
                        llm_file.write(input_res + "\n")

        if os.path.exists("temp_code"):
            os.remove("temp_code")
