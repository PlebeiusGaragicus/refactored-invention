# from src.constructs.test_graph import TestGraph
# from src.constructs.ollama_graph import OllamaGraph
# ALL_CONSTRUCTS = [TestGraph, OllamaGraph]


import logging
from typing import Annotated, Literal
from pathlib import Path

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import add_messages

import streamlit as st


def all_constructs():
    from src.constructs.test_graph import TestGraph
    from src.constructs.ollama_graph import OllamaGraph

    return [TestGraph, OllamaGraph]



class PlebGraph:
    """ This is the base class for all graphs in PlebChat! """

    @classmethod
    def interface_config(cls):
        raise NotImplementedError("interface_config() must be implemented in the subclass")

    @classmethod
    def build_graph(cls) -> CompiledGraph:
        raise NotImplementedError("build_graph() must be implemented in the subclass")

    @classmethod
    def save_diagram(cls):
        file = Path().parent / "assets" / f"{cls.name}_diagram.jpeg"
        img = cls.build_graph().get_graph().draw_mermaid_png()
        with open(file, "wb") as f:
            f.write(img)

    @classmethod
    def print_image(cls):
        file = Path().parent / "assets" / f"{cls.name}_diagram.jpeg"
        if not file.exists():
            cls.save_diagram()
        st.image( str(file) )


    @classmethod
    async def run_graph(cls, thought_container, bot_reply_chatmessage, status_expander):
        graph_config = RunnableConfig()
        graph_config['hyperparameters'] = st.session_state.graph_hyperparameters
        graph_config['metadata'] = {"conversation_id": st.session_state.session_id}
        graph_input = {"input": st.session_state.input, "messages": st.session_state.convo_history}
        graph = cls.build_graph()

        streamed_chunks = ""
        current_node = None
        current_writer = bot_reply_chatmessage.empty()
        thought_writer = None
        async for event in graph.astream_events(
                                input=graph_input,
                                config=graph_config,
                                version='v1',
                                # stream_mode='values' # TODO - find documentation for this ... probably under .stream()
                            ):
            status_expander.write(event['event'])
            status_expander.update(label=f":orange[Running:] :red[{event['event']}]")

            ### NOTE: This tries to get the final output of the graph
            ### I'm not otherwise sure how to get it when calling graph.astream_events()
            if event['event'] == "on_chain_end":
                if event['name'] == "LangGraph":
                    last_node = event['data']['output'].keys()
                    # get the first key
                    last_key = list(last_node)[0]
                    last_message = event['data']['output'].get(last_key)['messages'][0].content

            if event['event'] != current_node:
                streamed_chunks = ""
                current_node = event['event']
                # logging.debug(current_node)
                logging.debug(event)

                node_writer = thought_container.empty()
                node_writer.write(f"Node: {event['name']}: {current_node}")

                if current_node not in ["on_chat_model_stream", "on_llm_new_token"]:
                    continue

                thought_writer = thought_container.empty()

            node_type = event['metadata'].get('node_type', None)

            # AN LLM IS GIVING FEEDBACK TO THE USER!
            if node_type == "output":
                if event['data'].get('chunk', None):
                    streamed_chunks += event['data']['chunk'].content
                    current_writer.markdown(streamed_chunks)

            if node_type == "thought":
                if event['data'].get('chunk', None):
                    streamed_chunks += event['data']['chunk'].content
                    thought_writer.code(streamed_chunks)

        st.session_state.convo_history.append(HumanMessage(content=st.session_state.input))
        st.session_state.convo_history.append(AIMessage(content=last_message))

        # final_state = graph.get_state(config=graph_config)
        # logging.error(final_state)


# NODE METADATA
## this_config['metadata']['node_type'] = "output" | "thought"
