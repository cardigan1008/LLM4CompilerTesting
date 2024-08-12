import json
import os
import re
import subprocess
import sys
import random
import time
from together import Together
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generator.templates import generate_templates

load_dotenv()

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

features = [
    "Sorting",
    "Searching",
    "Filtering",
    "Calculating",
    "Parsing",
    "Compiling",
    "Tokenizing",
    "Optimizing",
    "Transforming",
    "Indexing",
    "Hashing",
    "Encrypting",
    "Decrypting",
    "Analyzing",
    "Mapping",
    "Reducing",
    "Collecting",
    "Merging",
    "Splitting",
    "Joining",
    "Rendering",
    "Translating",
    "Interpreting",
    "Encoding",
    "Decoding",
    "Synthesizing",
    "Rendering",
    "Clustering",
    "Classifying",
    "Regressing",
    "Estimating",
    "Predicting",
    "Simulating",
    "Modeling",
    "Quantifying",
    "Measuring",
    "Sorting",
    "Filtering",
    "Summarizing",
    "Aggregating",
    "Distributing",
    "Balancing",
    "Loading",
    "Storing",
    "Caching",
    "Buffering",
    "Streaming",
    "Reading",
    "Writing",
    "Logging",
    "Profiling",
    "Monitoring",
    "Scaling",
    "Sharding",
    "Partitioning",
    "Merging",
    "Concatenating",
    "Resampling",
    "Subsampling",
    "Batching",
    "Normalizing",
    "Standardizing",
    "Calibrating",
    "Aligning",
    "Projecting",
    "Embedding",
    "Flattening",
    "Expanding",
    "Shrinking",
    "Trimming",
    "Padding",
    "Cropping",
    "Segmenting",
    "Annotating",
    "Labeling",
    "Tagging",
    "Tracking",
    "Detecting",
    "Recognizing",
    "Matching",
    "Scanning",
    "Indexing",
    "Hashing",
    "Encrypting",
    "Decrypting",
    "Parsing",
    "Compiling",
    "Tokenizing",
    "Optimizing",
    "Transforming",
    "Interpreting",
    "Rendering",
    "Translating",
    "Analyzing",
    "Simulating",
    "Modeling",
    "Predicting",
    "Estimating",
    "Classifying",
    "Clustering",
]

styles = [
    "Exciting",
    "Boring",
    "Elegant",
    "Efficient",
    "Verbose",
    "Concise",
    "Readable",
    "Compact",
    "Obfuscated",
    "Clear",
    "Abstract",
    "Concrete",
    "Declarative",
    "Imperative",
    "Functional",
    "Object-Oriented",
    "Procedural",
    "Modular",
    "Dynamic",
    "Static",
    "Typed",
    "Untyped",
    "High-Level",
    "Low-Level",
    "Optimized",
    "Unoptimized",
    "Parallel",
    "Sequential",
    "Concurrent",
    "Linear",
    "Asynchronous",
    "Synchronous",
    "Recursive",
    "Iterative",
    "Event-Driven",
    "Stateful",
    "Stateless",
    "General",
    "Specific",
    "Robust",
    "Minimal",
    "Verbose",
    "Concise",
    "Readable",
    "Scalable",
    "Portable",
    "Flexible",
    "Adaptable",
    "Extensible",
    "Maintainable",
    "Testable",
    "Auditable",
    "Traceable",
    "Versioned",
    "Documented",
    "Instrumented",
    "Modular",
    "Structured",
    "Layered",
    "Interpreted",
    "Compiled",
    "Interactive",
    "Deterministic",
    "Non-Deterministic",
    "Abstract",
    "Concrete",
    "Optimized",
    "Unoptimized",
    "Parallel",
    "Sequential",
    "Concurrent",
    "Linear",
    "Asynchronous",
    "Synchronous",
    "Recursive",
    "Iterative",
    "Event-Driven",
    "Stateful",
    "Stateless",
    "General",
    "Specific",
    "Robust",
    "Minimal",
    "Verbose",
    "Scalable",
    "Portable",
    "Flexible",
    "Adaptable",
    "Extensible",
    "Maintainable",
    "Testable",
    "Auditable",
]

code_snippets = []
log_file_path = "generation_log.txt"
json_file_path = "code_snippets.json"
style_feature_file_path = "style_feature_info.json"
c_file_dir = "generated_c_files"
llm_responses_dir = "llm_responses"

# Initialize log file
with open(log_file_path, "a") as log_file:  # Append mode to continue logging
    log_file.write("Function generation log:\n")

# Load existing JSON file or initialize a new one
if os.path.exists(json_file_path):
    with open(json_file_path, "r") as outfile:
        code_snippets = json.load(outfile)
    valid_snippet_count = len(code_snippets)
else:
    valid_snippet_count = 0
    with open(json_file_path, "w") as outfile:
        json.dump([], outfile, indent=4)

# Load existing style-feature JSON file or initialize a new one
if os.path.exists(style_feature_file_path):
    with open(style_feature_file_path, "r") as sf_file:
        style_feature_info = json.load(sf_file)
else:
    style_feature_info = []
    with open(style_feature_file_path, "w") as sf_file:
        json.dump(style_feature_info, sf_file, indent=4)

# Create directories for .c files and LLM responses
os.makedirs(c_file_dir, exist_ok=True)
os.makedirs(llm_responses_dir, exist_ok=True)

# Initialize the start time for the first function
previous_time = time.time()

target_snippet_count = 999

while valid_snippet_count < target_snippet_count:
    feature = random.choice(features)
    style = random.choice(styles)

    content = generate_templates.format("Creal", feature=feature, style=style)

    response = client.chat.completions.create(
        model="codellama/CodeLlama-70b-Instruct-hf",
        messages=[
            {"role": "user", "content": content},
        ],
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["</s>", "[INST]"],
    )

    res = response.choices[0].message.content
    pattern = r"```C(.*?)```"
    match = re.search(pattern, res, re.DOTALL)

    if match:
        code_snippet = match.group(1).strip()
        if "scanf" in code_snippet or "printf" in code_snippet:
            print(
                f"Skipped code snippet due to scanf/printf usage for feature '{feature}' and style '{style}'."
            )
            continue

        # Generate unique filename with sequence number
        c_file_name = f"{valid_snippet_count + 1:03d}.c"
        c_file_path = os.path.join(c_file_dir, c_file_name)

        # Save the .c file with unique name
        with open(c_file_path, "w") as f:
            f.write(code_snippet)
            f.write("\n\n")
            f.write("#include <stdio.h>\n")
            f.write("int main() {\n")
            f.write("    return 0;\n")
            f.write("}\n")

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

            input_response = client.chat.completions.create(
                model="codellama/CodeLlama-70b-Instruct-hf",
                messages=[
                    {"role": "user", "content": content},
                    {"role": "assistant", "content": res},
                    {"role": "user", "content": generate_templates.format("Input")},
                ],
                max_tokens=512,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["</s>", "[INST]"],
            )
            input_res = input_response.choices[0].message.content
            pattern = r"\[.*?\]"
            matches = re.findall(pattern, input_res)
            if matches:
                io_pairs = []
                for match in matches:
                    function_signature = re.search(
                        r"(unsigned\s+)?(int|float|double|char|short|long\s+long|long)\s+(\w+)\s*\((.*?)\)",
                    )
                    if function_signature:
                        return_type = function_signature.group(1)
                        function_name = function_signature.group(2)
                        parameter_list = function_signature.group(3)

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
                            f.write(
                                f'    printf("%d\\n", {function_name}({inputs}));\n'
                            )
                            f.write("    return 0;\n")
                            f.write("}\n")

                        compile_result = subprocess.run(
                            [
                                "gcc",
                                "-fsanitize=undefined",
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
                                    timeout=30,
                                )
                                runtime_errors = run_result.stderr.decode()
                                if (
                                    "runtime error" in runtime_errors
                                    or "undefined" in runtime_errors
                                ):
                                    print(
                                        f"Undefined behavior detected in '{c_file_name}':\n{runtime_errors}"
                                    )
                                    continue
                                io_pairs.append(
                                    [
                                        str_cleaned_input,
                                        run_result.stdout.decode().strip(),
                                    ]
                                )
                            except subprocess.TimeoutExpired:
                                print(
                                    f"Execution timed out for '{c_file_name}'. The process was terminated."
                                )
                                continue
                        else:
                            print(
                                f"Compile error for input '{match}':\n{compile_result.stderr.decode()}"
                            )
                if io_pairs:
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

                    style_feature_data = {
                        "function": function_name,
                        "file": c_file_name,
                        "style_feature": {"style": style, "feature": feature},
                    }
                    style_feature_info.append(style_feature_data)

                    current_time = time.time()
                    time_interval = current_time - previous_time
                    previous_time = current_time
                    log_entry = (
                        f"func{valid_snippet_count}: {time_interval / 60:.2f} min"
                    )
                    with open(log_file_path, "a") as log_file:
                        log_file.write(log_entry + "\n")

                    with open(json_file_path, "r+") as outfile:
                        data = json.load(outfile)
                        data.append(snippet_data)
                        outfile.seek(0)
                        json.dump(data, outfile, indent=4)

                    with open(style_feature_file_path, "w") as sf_file:
                        json.dump(style_feature_info, sf_file, indent=4)

                    # Save the LLM response and input to a file
                    llm_response_path = os.path.join(
                        llm_responses_dir, f"{c_file_name}_llm_response.txt"
                    )
                    with open(llm_response_path, "w") as llm_file:
                        llm_file.write("User Input (First Request):\n")
                        llm_file.write(content + "\n\n")
                        llm_file.write("LLM Response (First Response):\n")
                        llm_file.write(res + "\n\n")
                        llm_file.write("User Input (Second Request):\n")
                        llm_file.write(generate_templates.format("Input") + "\n\n")
                        llm_file.write("LLM Response (Second Response):\n")
                        llm_file.write(input_res + "\n")

            else:
                print(
                    f"No input pairs found for feature '{feature}' and style '{style}'."
                )

        else:
            print(
                f"Compile error for feature '{feature}' and style '{style}':\n{compile_result.stderr.decode()}"
            )

        if os.path.exists("temp_code"):
            os.remove("temp_code")

    else:
        print(f"No code snippet found for feature '{feature}' and style '{style}'.")

print(f"Log entries saved to {log_file_path}")
print(f"Code snippets and .c files saved to {json_file_path} and {c_file_dir}")
print(f"Style-feature information saved to {style_feature_file_path}")
print(f"LLM responses saved to {llm_responses_dir}")
