from enum import Enum
import os


# Enum for different LLM models
class LLMModel(Enum):
    TOGETHER_AI = "together_ai"
    OPEN_AI = "open_ai"


# Configuration for API
MODEL_NAME = {
    LLMModel.TOGETHER_AI: "codellama/CodeLlama-34b-Instruct-hf",
    LLMModel.OPEN_AI: "gpt-4o-mini",
}
MAX_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.7
TOP_K = 50
REPETITION_PENALTY = 1
STOP = ["</s>", "[INST]"]

# Number of valid C functions to be generated
NUM_FUNCTIONS = 10000

DIR_ANGHA_BATCHES="batches"

# Path to the directory where the results will be saved
DIR_RESULTS = "results/results_openai_new"

PATH_LOG_TIME_FILE = os.path.join(DIR_RESULTS, "generation_time_log.txt")
PATH_LOG_FAILURE_FILE = os.path.join(DIR_RESULTS, "generation_failure_log.txt")
PATH_JSON_FILE = os.path.join(DIR_RESULTS, "code_snippets.json")
DIR_C_FILES = os.path.join(DIR_RESULTS, "generated_c_functions")
DIR_LLM_RESPONSES = os.path.join(DIR_RESULTS, "llm_responses")

# Prompt for role description
PROMPT_ROLE = (
    "You are working on a project that requires you to generate C functions. "
    "These functions will be used to test the C compiler. "
    "So make sure the functions are rich in C features and complexity to trigger interesting compiler internal behaviors like optimizations. "
)

PROMPT_CODE = (
    "Convert the given C program to one compilable C function that takes integer inputs and returns an integer: "
    "```c\n"
    "{code_snippet}\n"
    "```"
    "Instructions: "
    "a. It does not contain any other function calls. "
    "b. It is pure, meaning it has deterministic outputs and has no side effects. "
    "c. It takes only numeric input types and has a numeric return type. "
    "Note: "
    "a. When we say numeric, we mean int, long, long long, short, char, unsigned int, unsigned long, unsigned long long, unsigned short, unsigned char. "
    "b. Please only generate one function at a time without any explanation. You are not allowed to generate more than one function at a time. "
    "c. You can only keep necessary struct definitions and global variables used in the function. Remove all other unnecessary struct definitions and global variables. "
    "Below is an example of conversion. To avoid redundancy, please ensure your proposed function is distinct from the transformed function and avoid generating the same function: "
    """-------------------Original-------------------
    #define NULL ((void*)0)
    typedef unsigned long size_t;  // Customize by platform.
    typedef long intptr_t; typedef unsigned long uintptr_t;
    typedef long scalar_t__;  // Either arithmetic or pointer type.
    /* By default, we understand bool (as a convenience). */
    typedef int bool;
    #define false 0
    #define true 1

    /* Forward declarations */
    typedef  struct TYPE_4__   TYPE_1__ ;

    /* Type definitions */
    struct TYPE_4__ {{scalar_t__ nalloc; scalar_t__ len; char* body; }} ;
    typedef  TYPE_1__ Buffer ;

    /* Variables and functions */
    int realloc_body(TYPE_1__*) ;

    void buf_write(Buffer *b, char c) {{
        if (b->nalloc == (b->len + 1))
            realloc_body(b);
        b->body[b->len++] = c;
    }}
    -------------------Transformed-------------------
    #include <stdlib.h>

    typedef struct {{
        size_t nalloc;
        size_t len;
        char *body;
    }} Buffer;

    int buf_write(int nalloc, int len, char *body, char c) {{
        Buffer b;
        b.nalloc = nalloc;
        b.len = len;
        b.body = body;

        if (b.nalloc == (b.len + 1)) {{
            b.nalloc *= 2;
            b.body = realloc(b.body, b.nalloc);
        }}

        b.body[b.len++] = c;
        return b.len;
    }}"""
    
)

# Prompt for the task of generating a C function
PROMPT_GENERATE = (
    "Please generate a C function that has over 30 lines of code by adding the feature {feature} in a {style} style. "
    "Instructions: "
    "a. It takes only numeric input types and has a numeric return type. "
    "b. It dose not contain any other function calls. "
    "c. It is pure, meaning it has deterministic outputs and has no side effects. "
    "d. Be creative! The function should be complex and use as many C language features as possible. "
    "Note: "
    "a. When we say numeric, we mean int, long, long long, short, char, unsigned int, unsigned long, unsigned long long, unsigned short, unsigned char. "
    "b. Please only generate one function at a time without any explanation. You are not allowed to generate more than one function at a time. "
    "c. Complexity is key! You can use non-constant-bounded loops or some high-level memory operations. "
)

# Prompt for the task of generating input pairs for a C function
PROMPT_INPUT = (
    "For the provided function, please generate the inputs that cover all the possible branches. "
    "Instructions: "
    "a. Wrap the each possible input in a list. For example: [input1], [input2], [input3]... "
    "b. Make sure each possible input corresponds to the arguments of the function. For example, the number of inputs should match the number of arguments. "
)

# List of features that guide the generation of C functions
FEATURES = [
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

# FEATURES = [
#     "Matrix Determinant Calculation",
#     "Linked List Reversal",
#     "Binary Tree Depth Calculation",
#     "QuickSort Algorithm",
#     "MergeSort Algorithm",
#     "HeapSort Algorithm",
#     "Dijkstra's Shortest Path Algorithm",
#     "A* Pathfinding Algorithm",
#     "Knapsack Problem Solver",
#     "Graph Coloring Problem",
#     "Levenshtein Distance Computation",
#     "Floyd-Warshall All-Pairs Shortest Path",
#     "Kruskal's Minimum Spanning Tree Algorithm",
#     "Prim's Minimum Spanning Tree Algorithm",
#     "Breadth-First Search for Graphs",
#     "Depth-First Search for Graphs",
#     "Topological Sort of a Directed Graph",
#     "Bellman-Ford Algorithm for Shortest Paths",
#     "Boyer-Moore String Search Algorithm",
#     "Rabin-Karp String Matching Algorithm",
#     "Permutations Generator",
#     "Combinations Generator",
#     "Huffman Coding for Data Compression",
#     "Lempel-Ziv Compression Algorithm",
#     "RSA Encryption Algorithm",
#     "AES Encryption Routine",
#     "SHA-256 Hashing Function",
#     "Bubble Sort with Optimization",
#     "Circular Queue Implementation",
#     "Double-Ended Queue Implementation",
#     "Red-Black Tree Insertion and Balancing",
#     "AVL Tree Insertion and Balancing",
#     "B-tree Insertion and Search",
#     "Fibonacci Heap Operations",
#     "Disjoint Set Union-Find Algorithm",
#     "Tarjan's Strongly Connected Components Algorithm",
#     "Ford-Fulkerson Algorithm for Maximum Flow",
#     "Backtracking Solver for Sudoku",
#     "N-Queens Problem Solver",
#     "Expression Parsing and Evaluation",
#     "Regular Expression Matching with Backtracking",
#     "Simulated Annealing for Optimization Problems",
#     "Newton-Raphson Method for Finding Roots",
#     "Gaussian Elimination for Solving Linear Equations",
#     "LU Decomposition of a Matrix",
#     "FFT (Fast Fourier Transform) Implementation",
#     "Convex Hull Construction using Graham's Scan",
#     "Kadane's Algorithm for Largest Sum Contiguous Subarray",
#     "Karatsuba Multiplication for Large Integers",
#     "Sieve of Eratosthenes for Prime Generation",
#     "Segment Tree with Lazy Propagation",
#     "Binary Indexed Tree (Fenwick Tree) Operations",
#     "Dynamic Time Warping for Time Series Analysis",
#     "Cycle Detection in a Directed Graph",
#     "Manacher's Algorithm for Longest Palindromic Substring",
#     "Minimum Cut in a Graph",
#     "Chinese Remainder Theorem Solver",
#     "Pollard's Rho Algorithm for Integer Factorization",
#     "Eulerian Path/Circuit Finding",
#     "Hamiltonian Path/Circuit Finding",
#     "Longest Increasing Subsequence",
#     "Bitonic Sort Implementation",
#     "Bucket Sort for Integer Keys",
#     "Radix Sort Implementation",
#     "Counting Sort Implementation",
#     "Shell Sort Implementation",
#     "Pancake Sorting Algorithm",
#     "Bogo Sort (as an Example of a Inefficient Algorithm)",
#     "Gale-Shapley Algorithm for Stable Marriage Problem",
#     "Moore's Voting Algorithm for Majority Element",
#     "KMP Algorithm for Substring Search",
#     "Z Algorithm for String Matching",
#     "Activity Selection Problem Solver",
#     "Job Scheduling Problem Solver",
#     "Interval Scheduling Maximization",
#     "Dining Philosophers Problem Simulation",
#     "Reader-Writer Problem Solution",
#     "Producer-Consumer Problem Solution",
#     "Banker's Algorithm for Deadlock Avoidance",
#     "Lamport's Bakery Algorithm for Mutual Exclusion",
#     "Peterson's Algorithm for Mutual Exclusion",
#     "Binary Exponentiation for Fast Exponentiation",
#     "Miller-Rabin Primality Test",
#     "Extended Euclidean Algorithm for Inverses",
#     "Modular Exponentiation",
#     "Trie Structure for String Storage and Retrieval",
#     "Suffix Array Construction",
#     "Burrows-Wheeler Transform for Text Compression",
#     "Suffix Tree Construction"
# ]

# List of styles that guide the generation of C functions
STYLES = [
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
