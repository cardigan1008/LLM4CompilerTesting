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
        pattern = r"(unsigned\s+)?(int|char|short|long\s+long|long)\s+(\w+)\s*\((.*?)\)"
        match = re.search(pattern, code_snippet)
        if match:
            return_type = match.group(2)
            function_name = match.group(3)
            parameter_list = match.group(4)

            # Extract parameter types
            parameter_types = (
                [param.strip().split(" ")[0] for param in parameter_list.split(",")]
                if parameter_list
                else []
            )

            return {
                "return_type": return_type,
                "function_name": function_name,
                "parameter_types": parameter_types,
                "function": code_snippet,
            }
        return None
