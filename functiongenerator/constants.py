from enum import Enum
import os


# Enum for different LLM models
class LLMModel(Enum):
    TOGETHER_AI = "together_ai"
    OPEN_AI = "open_ai"


# Configuration for API
MODEL_NAME = {
    LLMModel.TOGETHER_AI: "codellama/CodeLlama-34b-Instruct-hf",
    LLMModel.OPEN_AI: "gpt-4o",
}
MAX_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.7
TOP_K = 50
REPETITION_PENALTY = 1
STOP = ["</s>", "[INST]"]

# Number of valid C functions to be generated
NUM_FUNCTIONS = 5

# Path to the directory where the results will be saved
DIR_RESULTS = "results_openai"

PATH_LOG_FILE = os.path.join(DIR_RESULTS, "generation_log.txt")
PATH_JSON_FILE = os.path.join(DIR_RESULTS, "code_snippets.json")
DIR_C_FILES = os.path.join(DIR_RESULTS, "generated_c_functions")
DIR_LLM_RESPONSES = os.path.join(DIR_RESULTS, "llm_responses")


# Prompt for the task of generating a C function
PROMPT_GENERATE = (
    "Please generate a C function that has over 30 lines of code by adding the feature {feature} in a {style} style. "
    "Instructions: "
    "a. It takes only numeric input types and has a numeric return type. "
    "b. It dose not contain any other function calls, espeically I/O functions like printf or scanf or random functions. "
    "c. It is pure, meaning it has deterministic outputs and has no side effects. "
    "d. Please generate the code snippet that starts with ```C and ends with ```. "
    "e. Be creative! The function should use as many C language features as possible. "
    "f. The name of function should be unique, which can be achieved by including a number at the end of the function name. "
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
