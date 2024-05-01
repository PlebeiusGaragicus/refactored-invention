from typing import Annotated, Literal
from pathlib import Path

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import add_messages

import streamlit as st

from src.interface import (
    Colors,
    cprint,
    numeric_parameter,
    options_parameter,
    boolean_parameter,
    text_parameter,
    prompt_parameter
)

from src.constructs import PlebGraph

class State(TypedDict):
    input: str
    messages: Annotated[list, add_messages]




class OllamaGraph(PlebGraph):
    """
# Ollama Graph

This is the simplest graph you can make - just one node that calls an Ollama model."""
    name: str = "Ollama"
    avatar: str = "🦙"

    @classmethod
    def interface_config(self):
        # TODO - try to list the available models... perhaps on app load?
        MODEL_OPTIONS = ['llama:8b', 'gemma:2b', 'mistral:7b', 'dolphin-mistral:latest']

        return {
            "graph_name": "Example Graph",
            "widgets": [
                # TODO rename these to - numeric_parameter, options_parameter, boolean_parameter, text_parameter
                numeric_parameter("llm_temperature", 0.0, 1.0, default=0.8, help="The temperature of the LLM"),
                options_parameter("llm_model", MODEL_OPTIONS, default="gemma:2b", help="The LLM model to use"),
                prompt_parameter("Behaviour prompt", default="Initial remark...", help="The prompt for the generate node"),
            ]
        }


    @classmethod
    def build_graph(cls) -> CompiledGraph:

        from .call_ollama import call_ollama

        graph_builder = StateGraph(State)

        graph_builder.add_node("call_ollama", call_ollama)
        graph_builder.set_entry_point("call_ollama")
        graph_builder.set_finish_point("call_ollama")
        # graph_builder.add_edge("call_ollama", END)

        graph: CompiledGraph = graph_builder.compile()
        return graph


