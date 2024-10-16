import json
import os
import random


def get_printf_format(return_type):
    """
    Returns the correct printf format specifier based on the return type.

    Parameters:
        return_type (str): The return type of the function (e.g., "int", "float", "double", "char").

    Returns:
        str: The corresponding printf format specifier.
    """
    if return_type in ["int", "short", "long", "long long"]:
        return "%d"  # Integer format
    elif return_type == "unsigned int":
        return "%u"  # Unsigned integer format
    elif return_type in ["uint8_t", "uint16_t", "uint32_t", "uint64_t"]:
        return "%u"  # Unsigned integer format
    elif return_type in ["int8_t", "int16_t", "int32_t", "int64_t"]:
        return "%d"  # Signed integer format
    elif return_type == "size_t":
        return "%zu"  # Size type format
    elif return_type == "ptrdiff_t":
        return "%td"  # Pointer difference format
    elif return_type == "float":
        return "%f"  # Float format
    elif return_type == "double":
        return "%lf"  # Double format
    elif return_type == "char":
        return "%c"  # Character format
    elif return_type == "unsigned char":
        return "%c"  # Unsigned character format
    else:
        raise ValueError(f"Unsupported return type: {return_type}")

def extract_random_function_from_batches(batch_dir):
    """
    Randomly selects and returns one function from multiple JSON batch files.

    Parameters:
        batch_dir (str): The directory containing the batch JSON files.

    Returns:
        dict: A dictionary representing a randomly selected function.
    """
    # List all JSON batch files in the directory
    batch_files = [f for f in os.listdir(batch_dir) if f.endswith('.json')]
    
    if not batch_files:
        raise ValueError("No batch files found in the specified directory.")

    # Randomly select one batch file
    random_batch_file = random.choice(batch_files)
    random_batch_path = os.path.join(batch_dir, random_batch_file)
    
    # Load the selected batch file
    with open(random_batch_path, "r", encoding="utf-8") as batch_json:
        functions = json.load(batch_json)
    
    # Randomly select one function from the batch
    random_function = random.choice(functions)
    
    return random_function
