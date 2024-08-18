from abc import ABC, abstractmethod
from openai import OpenAI
from together import Together

from functiongenerator.constants import (
    MAX_TOKENS,
    MODEL_NAME,
    PROMPT_ROLE,
    REPETITION_PENALTY,
    STOP,
    TEMPERATURE,
    TOP_K,
    TOP_P,
    LLMModel,
)


class LLMClient(ABC):
    @abstractmethod
    def create_chat_completion(self, messages, **kwargs):
        pass


class TogetherAIClient(LLMClient):
    def __init__(self, api_key):
        self.client = Together(api_key=api_key)

    def create_chat_completion(self, messages, **kwargs):
        """
        Create a chat completion with alternating roles in the conversation.

        Parameters:
            messages (list): A list of strings representing the conversation context.
                            Alternates roles between 'user' and 'assistant'.
            model (str): The model to use for chat completion.
            max_tokens (int): Maximum number of tokens in the completion.
            temperature (float): Sampling temperature.
            top_p (float): Nucleus sampling probability.
            top_k (int): Top-k sampling parameter.
            repetition_penalty (float): Repetition penalty.
            stop (list): List of stopping sequences.

        Returns:
            response: The LLM response.
        """
        model = kwargs.get("model", MODEL_NAME[LLMModel.TOGETHER_AI])
        max_tokens = kwargs.get("max_tokens", MAX_TOKENS)
        temperature = kwargs.get("temperature", TEMPERATURE)
        top_p = kwargs.get("top_p", TOP_P)
        top_k = kwargs.get("top_k", TOP_K)
        repetition_penalty = kwargs.get("repetition_penalty", REPETITION_PENALTY)
        stop = kwargs.get("stop", STOP)

        # Initialize the conversation with alternating roles
        conversation = [{"role": "system", "content": PROMPT_ROLE}]
        for i, msg in enumerate(messages):
            role = "user" if i % 2 == 0 else "assistant"
            conversation.append({"role": role, "content": msg})

        # Create the chat completion
        response = self.client.chat.completions.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            stop=stop,
        )

        return response
    

class OpenAIClient(LLMClient):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def create_chat_completion(self, messages, **kwargs):
        model = kwargs.get("model", MODEL_NAME[LLMModel.OPEN_AI])
        max_tokens = kwargs.get("max_tokens", MAX_TOKENS)
        temperature = kwargs.get("temperature", TEMPERATURE)
        top_p = kwargs.get("top_p", TOP_P)
        stop = kwargs.get("stop", STOP)

        conversation = []
        for i, msg in enumerate(messages):
            role = "user" if i % 2 == 0 else "assistant"
            conversation.append({"role": role, "content": msg})
        
        response = self.client.chat.completions.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=stop,
        )
    
        return response


class LLMClientFactory:
    @staticmethod
    def create_client(client_type, api_key):
        """
        Create a client for the specified LLM model.

        Parameters:
            client_type (LLMModel): The LLM model type.
            api_key (str): The API key for the LLM model.

        Returns:
            LLMClient: The LLM client.
        """
        if client_type.value == LLMModel.TOGETHER_AI.value:
            return TogetherAIClient(api_key)   
        elif client_type.value == LLMModel.OPEN_AI.value:
            return OpenAIClient(api_key)     
        else:
            raise ValueError(f"Invalid client type: {client_type}")
