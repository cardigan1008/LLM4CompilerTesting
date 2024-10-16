import json
import os

json_file_path = "function_io.json"
output_dir = "functions"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(json_file_path, "r", encoding="utf-8") as f:
    functions_data = json.load(f)

for function in functions_data:
    src_file = function.get("src_file", "")
    if not src_file:
        continue
    
    file_name = os.path.basename(src_file)
    
    output_file_path = os.path.join(output_dir, file_name)
    
    function_code = function.get("function", "")
    
    if function_code:
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(function_code)

