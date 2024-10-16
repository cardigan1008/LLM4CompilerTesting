import argparse
import os
import json
from tqdm import tqdm

def extract_functions_by_batch(dir_angha, output_dir, batch_size=10000):
    """
    Extracts functions from the dataset and saves them into multiple JSON files by batch.

    Parameters:
        dir_angha (str): The directory containing the dataset.
        output_dir (str): The directory where the batch JSON files will be saved.
        batch_size (int): The number of functions to store in each batch file.
    
    Returns:
        None
    """
    functions = []
    file_count = 0
    total_count = 0
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Walk through the directory structure with a progress bar
    for root, _, files in tqdm(os.walk(dir_angha), desc="Extracting functions"):
        for file in files:
            if file.endswith(".c"):
                # Read each .c file and append the content as a single entry
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    code = f.read()
                    functions.append({
                        "file_name": file,
                        "file_path": os.path.join(root, file),
                        "content": code
                    })  # Store file name, path, and content as a dict
                
                total_count += 1
                
                # Save the batch if we've reached the batch size
                if total_count % batch_size == 0:
                    batch_file = os.path.join(output_dir, f"functions_batch_{file_count}.json")
                    with open(batch_file, "w", encoding="utf-8") as batch_json:
                        json.dump(functions, batch_json, indent=4, ensure_ascii=False)
                    functions = []  # Clear the list for the next batch
                    file_count += 1
    
    # Save the remaining functions if any
    if functions:
        batch_file = os.path.join(output_dir, f"functions_batch_{file_count}.json")
        with open(batch_file, "w", encoding="utf-8") as batch_json:
            json.dump(functions, batch_json, indent=4, ensure_ascii=False)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Extract functions from the dataset and save them into multiple JSON batch files.")
    parser.add_argument("dir_angha", help="The directory containing the dataset.")
    parser.add_argument("output_dir", help="The directory where the batch JSON files will be saved.")
    parser.add_argument("--batch_size", type=int, default=10000, help="The number of functions to store in each batch file. Default is 10,000.")

    args = parser.parse_args()

    # Call the function with the provided arguments
    extract_functions_by_batch(args.dir_angha, args.output_dir, args.batch_size)

if __name__ == "__main__":
    main()
