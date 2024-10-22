import json
import os
import re
import sys
import time

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functiongenerator.validator import Validator
from templates import Templates
from constants import (
    DIR_ANGHA_BATCHES,
    NUM_FUNCTIONS,
    PATH_LOG_COMPLILATION_FAILED_FUNCTIONS,
    PATH_LOG_FAILURE_FILE,
    PATH_LOG_TIME_FILE,
    PATH_JSON_FILE,
    DIR_RESULTS,
    DIR_C_FILES,
    DIR_LLM_RESPONSES,
    PATH_LOG_UNSUPPORTED_SIGS_FUNCTIONS,
    LLMModel,
)
from utils.llm import LLMClientFactory
from utils.utils import extract_random_function_from_batches

DEBUG = False

load_dotenv()

os.environ['all_proxy'] = ''
os.environ['ALL_PROXY'] = ''
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

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

invalid_snippet_count = 0

code_snippets = []

# Initialize the start time for the first function
previous_time = time.time()

while valid_snippet_count < NUM_FUNCTIONS:
    angha_function = extract_random_function_from_batches(DIR_ANGHA_BATCHES)["content"]
    generation_query = Templates.format("CodeSnippet", code_snippet=angha_function)
    response = client.create_chat_completion([generation_query])

    generation_res = response.choices[0].message.content
    pattern = r"```(?:[Cc])?(.*?)```"
    match = re.search(pattern, generation_res, re.DOTALL)

    print("generation response:" + generation_res)

    if match:
        code_snippet = match.group(1).strip()
        if "scanf" in code_snippet or "printf" in code_snippet:
            invalid_snippet_count += 1
            with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                log_file.write(f"func{invalid_snippet_count}: Contains scanf or printf\n")
            continue
            
        if not Validator.has_minimum_lines(code_snippet):
            invalid_snippet_count += 1
            with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                log_file.write(f"func{invalid_snippet_count}: Too few lines after removing comments\n")
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

        if Validator.is_compilable(c_file_path):
            function_data = Validator.extract_function_signature(code_snippet)
            if function_data:
                code_snippets.append(function_data)

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
                    data.append(function_data)
                    outfile.seek(0)
                    json.dump(data, outfile, indent=4)

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
                if DEBUG:
                    with open(PATH_LOG_UNSUPPORTED_SIGS_FUNCTIONS, "a") as log_file:
                        log_file.write(f"Unsupported signature:\n {code_snippet}\n")
                with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                    log_file.write(f"func{invalid_snippet_count}: Function signature not supported\n")
        else:
            invalid_snippet_count += 1
            if DEBUG:
                with open(PATH_LOG_COMPLILATION_FAILED_FUNCTIONS, "a") as log_file:
                    log_file.write(f"Compilation failed:\n {code_snippet}\n")
            with open(PATH_LOG_FAILURE_FILE, "a") as log_file:
                log_file.write(f"func{invalid_snippet_count}: Compilation failed\n")
