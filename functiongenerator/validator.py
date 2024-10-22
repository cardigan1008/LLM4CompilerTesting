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

        pattern = (
            r"(const\s+)?(unsigned\s+|signed\s+)?"
            r"(void|int|char|short|long\s+long|long|float|double|"
            r"size_t|uint\d+_t|int\d+_t|bool|double)\s+(\w+)\s*\((.*?)\)"
        )
        match = re.search(pattern, code_snippet, flags=re.DOTALL | re.MULTILINE)

        if match:
            return_type = f"{match.group(1) or ''}{match.group(2) or ''}{match.group(3)}".strip()
            function_name = match.group(4)
            parameter_list = match.group(5).strip()

            if parameter_list:
                parameter_types = [param.strip() for param in parameter_list.split(",")]

                for param in parameter_types:
                    if (
                        "struct" in param or "union" in param or 
                        not re.match(r"(const\s+)?(unsigned\s+|signed\s+)?"
                                     r"(void|int|char|short|long\s+long|long|float|double|"
                                     r"size_t|uint\d+_t|int\d+_t|bool)(\s*\*?\s*)?", param)
                    ):
                        return None

                parameter_types = [
                    " ".join(param.split()[:-1])
                    if len(param.split()) > 1 else param
                    for param in parameter_types
                ]
            else:
                parameter_types = []

            return {
                "return_type": return_type,
                "function_name": function_name,
                "parameter_types": parameter_types,
                "function": code_snippet,
            }
        return None

    @staticmethod
    def remove_comments(code_snippet):
        """
        Remove comments and empty lines from the given C code snippet.
        """
        code_without_comments = re.sub(r"//.*?$|/\*.*?\*/", "", code_snippet, flags=re.DOTALL | re.MULTILINE)
        lines = [line.strip() for line in code_without_comments.splitlines() if line.strip()]
        return lines

    @staticmethod
    def has_minimum_lines(code_snippet, min_lines=5):
        """
        Check if the given C code snippet has at least the specified number of non-empty lines after removing comments.
        """
        lines = Validator.remove_comments(code_snippet)
        return len(lines) >= min_lines
