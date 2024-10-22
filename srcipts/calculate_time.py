import sys
import re
import statistics

def extract_times(file_path):
    times = []
    # Regular expression to match the pattern: "funcN: T s"
    pattern = r'func\d+:\s+([\d.]+)\s+s'
    
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                times.append(float(match.group(1)))
    
    return times

def calculate_statistics(times):
    max_time = max(times)
    min_time = min(times)
    median_time = statistics.median(times)
    mean_time = statistics.mean(times)
    
    return max_time, min_time, median_time, mean_time

def main(file_path):
    times = extract_times(file_path)
    
    if not times:
        print("No valid time data found.")
        return
    
    max_time, min_time, median_time, mean_time = calculate_statistics(times)
    
    print(f"Max Time: {max_time:.6f} s")
    print(f"Min Time: {min_time:.6f} s")
    print(f"Median Time: {median_time:.6f} s")
    print(f"Mean Time: {mean_time:.6f} s")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        main(sys.argv[1])
