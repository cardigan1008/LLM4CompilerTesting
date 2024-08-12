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
