import os
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

from langchain_community.chat_models import ChatOllama
from langchain_experimental.llms.ollama_functions import OllamaFunctions


class Colors():
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

def cprint(string: str, color: Colors, endl='\n'):
    print_this = f'\033[1;3{color}m' + string + '\033[0m'
    print(print_this, end=endl)



class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


model="dolphin-mistral:latest"
llm = OllamaFunctions(model=model)
# llm = ChatOllama(model=model)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")

graph = graph_builder.compile()

















while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        cprint("Goodbye!", Colors.RED)
        break
    if user_input.strip() == "":
        continue
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            cprint("Assistant:", Colors.BLUE, end=" ")
            cprint(value["messages"][-1].content, Colors.GREEN)
