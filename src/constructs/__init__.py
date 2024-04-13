# class BaseConstruct:
#     def show_settings():
#         raise NotImplementedError("show_settings() must be implemented in the child class")
    
#     def run_prompt():
#         raise NotImplementedError("run_prompt() must be implemented in the child class")

from src.constructs.chain_ollama import OllamaSimpleChain
from src.constructs.chain_openai import OpenAIChain

ALL_CONSTRUCTS = [OllamaSimpleChain, OpenAIChain]

