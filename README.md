# LLM4CompilerTesting

Using Large Language Models (LLMs) to conduct compiler testing.

## Setup Environment

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/LLM4CompilerTesting.git
cd LLM4CompilerTesting
```

### Step 2: Prepare Your API Key

If you are using Together AI as the LLM provider:


```bash
echo TOGETHER_API_KEY=<your_together_api_key> > .env 
```

Replace <your_together_api_key> with your actual Together AI API key.

### Step 3: Install Dependencies

Ensure you have Python 3.10 installed. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Project

To start generating and testing functions with the LLM:

```bash
python3 functiongenerator/generator.py
```

This will begin the process of generating C functions, compiling them, and checking for runtime behavior.
