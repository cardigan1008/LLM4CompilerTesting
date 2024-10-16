import os
import re
import subprocess


class Validator:
    @staticmethod
    def is_compilable(c_file_path):
        """
        Check if the C code in the given file can be compiled successfully using gcc.
        """
        compile_result = subprocess.run(
            ["gcc", "-o", "temp_code", c_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Clean up the temporary compiled file if it exists
        if os.path.exists("temp_code"):
            os.remove("temp_code")
        return compile_result.returncode == 0

    @staticmethod
    def extract_function_signature(code_snippet):
        """
        Extract the function signature from the given C code snippet.
        Returns a dictionary with return type, function name, and parameter types if valid, or None if not.
        """
        # Expanded pattern to include more primitive types and optional signed/unsigned
        pattern = r"(unsigned\s+|signed\s+)?(void|int|char|short|long\s+long|long|float|double)\s+(\w+)\s*\((.*?)\)"
        match = re.search(pattern, code_snippet)
        if match:
            return_type = match.group(2)
            function_name = match.group(3)
            parameter_list = match.group(4)

            # Extract parameter types, excluding complex types like structs
            if parameter_list:
                parameter_types = [param.strip() for param in parameter_list.split(",")]

                # Check if any parameter contains 'struct' or other non-primitive types
                for param in parameter_types:
                    # Allow only primitive types in the parameter list
                    if "struct" in param or not re.match(r"(unsigned\s+|signed\s+)?(void|int|char|short|long\s+long|long|float|double)", param):
                        return None

                # Only extract primitive types, ignoring variable names
                parameter_types = [param.split(" ")[-2:] if "unsigned" in param or "signed" in param else param.split(" ")[0] for param in parameter_types]

            else:
                parameter_types = []

            return {
                "return_type": return_type,
                "function_name": function_name,
                "parameter_types": parameter_types,
                "function": code_snippet,
            }
        return None
