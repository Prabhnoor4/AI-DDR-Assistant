from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    #abstract base class for LLM providers
    

    @abstractmethod
    def generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        #generate text from the LLM
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        #get the model name for caching purposes
        pass
