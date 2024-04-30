from typing import Annotated, Literal

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from src.interface import (
    Colors,
    cprint,
    numeric_parameter,
    options_parameter,
    boolean_parameter,
    text_parameter,
    prompt_parameter
)




class State(TypedDict):
    input: str
    messages: Annotated[list, add_messages]





def bad_route(state: State, config: RunnableConfig):
    cprint("\n--- NODE: bad_route() ---", Colors.MAGENTA)
    cprint("### THIS SHOULD NEVER HAPPEN!!! ###", Colors.RED)

    return {"messages": [AIMessage(content="I'm sorry, I don't understand that question.")]}



def build_graph(use_open_routing: bool):

    from src.constructs.test_graph.router import route_OpenAI, route_Ollama
    from src.constructs.test_graph.friendly_chatbot import friendly_chatbot
    from src.constructs.test_graph.vector_store import vectorstore


    # workflow = StateGraph(GraphState)
    graph_builder = StateGraph(State)


    graph_builder.add_node("vectorstore", vectorstore)
    graph_builder.add_edge("vectorstore", END)
    graph_builder.add_node("friendly_chatbot", friendly_chatbot)
    graph_builder.add_edge("friendly_chatbot", END)
    graph_builder.add_node("bad_route", bad_route)
    graph_builder.add_edge("bad_route", END)

    graph_builder.set_conditional_entry_point(
                    route_OpenAI if use_open_routing else route_Ollama,
                    {
                        "vectorstore": "vectorstore",
                        "friendly_chatbot": "friendly_chatbot",
                        "bad_route": "bad_route"
                    }
                )


    graph = graph_builder.compile()
    return graph



class TestGraph:
    """ This is the docstring to the graph class!  Whoopiee!"""
    name: str = "TestGraph"
    avatar: str = "🛠️"


    def interface_config(self):
        MODEL_OPTIONS = ['gemma:2b', 'mistral:7b', 'dolphin-mistral:latest', 'OpenAI']

        return {
            "graph_name": "Example Graph",
            "widgets": [
                # TODO rename these to - numeric_parameter, options_parameter, boolean_parameter, text_parameter
                numeric_parameter("llm_temperature", 0.0, 1.0, default=0.8, help="The temperature of the LLM"),
                options_parameter("llm_model", MODEL_OPTIONS, default="gemma:2b", help="The LLM model to use"),
                boolean_parameter("use_open_routing", default=False, help="Use OpenAI for routing"),
                text_parameter("Who is your daddy what what does he do?", default="a nerd!", help="Just answer the question..."),
                prompt_parameter("Generate node prompt", default="Initial remark...", help="The prompt for the generate node"),
                prompt_parameter("Reflect node prompt", default="back to back", help="The prompt for the reflect node"),
            ]
        }


    def invoke_graph(self, bot_reply_placeholder, thoughts):
        pass
