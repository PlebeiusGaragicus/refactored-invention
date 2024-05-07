import uuid

from typing import Annotated, Literal

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain.prompts import PromptTemplate

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from src.interface import Colors, color, reset_color, cprint, numeric_parameter, options_parameter, boolean_parameter, text_parameter, prompt_parameter
# create_slider, create_selectbox, create_checkbox, create_text_area


from src.constructs.test_graph import State



def vectorstore(state: State, config: RunnableConfig):
    cprint("\n--- NODE: vectorstore() ---", Colors.MAGENTA)

    # this_config = config
    # this_config['metadata']['node_type'] = "thought"

    return {"messages": [AIMessage(content="THE DATABASE IS NOT YET IMPLEMENTED!")]}
