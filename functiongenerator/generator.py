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
    PATH_LOG_FAILURE_FILE,
    PATH_LOG_TIME_FILE,
    PATH_JSON_FILE,
    DIR_RESULTS,
    DIR_C_FILES,
    DIR_LLM_RESPONSES,
    LLMModel,
)
from utils.llm import LLMClientFactory

load_dotenv()
# api_key = os.environ.get("TOGETHER_API_KEY")
# client = LLMClientFactory.create_client(LLMModel.TOGETHER_AI, api_key=api_key)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

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

invalid_snippet_count = 0

code_snippets = []

# Initialize the start time for the first function
previous_time = time.time()

while valid_snippet_count < NUM_FUNCTIONS:
    generation_query = Templates.format("Generate")
    response = client.create_chat_completion([generation_query])

    generation_res = response.choices[0].message.content
    pattern = r"```(?:[Cc])?(.*?)```"
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
            function_signature = re.search(
                r"(unsigned\s+)?(int|char|short|long\s+long|long)\s+(\w+)\s*\((.*?)\)",
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

                snippet_data = {
                        "function_name": function_name,
                        "parameter_types": parameter_types,
                        "return_type": return_type,
                        "function": code_snippet,
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
                with open(PATH_LOG_TIME_FILE, "a") as log_file:
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
            else:
                invalid_snippet_count += 1
                unsupported_signature = function_signature.group(0) if function_signature else "Unknown"
                with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                    log_file.write(f"func{invalid_snippet_count}: Function return type not supported: {unsupported_signature}\n")
        else:
            invalid_snippet_count += 1
            with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                log_file.write(f"func{invalid_snippet_count}: Compilation failed\n")

        if os.path.exists("temp_code"):
            os.remove("temp_code")
