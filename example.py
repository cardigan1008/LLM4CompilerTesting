import os
from together import Together
from dotenv import load_dotenv

load_dotenv()

client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

response = client.chat.completions.create(
    model="codellama/CodeLlama-13b-Instruct-hf",
    messages=[
        {
            "role": "user",
            "content": "Hello, I am a Python developer. Can you help me with a code snippet?"
        },
    ],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["</s>","[INST]"],
)

print(response.choices[0].message.content)
