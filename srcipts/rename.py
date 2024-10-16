import json
import random
import string
import re

def random_string(length=8):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def rename_function_name(data):
    keywords = ['if', 'else', 'while', 'for', 'switch', 'case', 'do', 'return', 'break', 'continue', 'goto', 'sizeof', 'typedef', 'struct', 'union', 'enum', 'static', 'const', 'volatile', 'register', 'extern', 'auto', 'signed', 'unsigned', 'void', 'char', 'short', 'int', 'long', 'float', 'double']
    function_pattern = re.compile(r'\b(unsigned\s+)?(int|char|short|long\s+long|long)\s+((?!' + '|'.join(keywords) + r'\b)\w+)\s*\((.*?)\)')
    for function in data:
        rand_str = random_string()

        origin_name = function["function_name"]
        new_name = f"{origin_name}_{rand_str}"
        function["function_name"] = new_name

        function["function"] = function["function"].replace(origin_name, new_name)

        functions_in_code = function_pattern.findall(function["function"])
        for match in functions_in_code:
            func_name = match[2]
            if func_name != new_name:
                rand_str = random_string()
                new_func_name = f"{func_name}_{rand_str}"
                function["function"] = function["function"].replace(func_name, new_func_name)

    return data

def rename_typedef_struct(data):
    typedef_struct_pattern = re.compile(r'\btypedef\s+struct\s*\{[^}]*\}\s*(\w+);')
    for function in data:
        typedefs = typedef_struct_pattern.findall(function["function"])
        for typedef in typedefs:
            rand_str = random_string()
            new_typedef = f"{typedef}_{rand_str}"
            function["function"] = function["function"].replace(typedef, new_typedef)

    return data

if __name__ == "__main__":
    data = json.load(open("code_snippets.json"))
    data = rename_function_name(data)
    data = rename_typedef_struct(data)
    json.dump(data, open("code_snippets_renamed.json", "w"), indent=4)
