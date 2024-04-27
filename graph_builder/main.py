import os
import uuid
import dotenv
import asyncio


import streamlit as st

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from .interface import Colors, color, reset_color, cprint, cput, change_color, build_interface
from .graph import build_graph, graph_parameter_widgets

# chat_model = enquiries.choose(f'{color(Colors.RED)}Select chatbot model{reset_color()}', model_options)


def main():

    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if 'convo_history' not in st.session_state:
        st.session_state.convo_history = []

    st.title("Langchain Graph Builder")
    st.write(f"Session ID: {st.session_state.session_id}")

    build_interface( graph_parameter_widgets() )


    if input := st.chat_input("User: "):
        # st.session_state.convo_history.append(HumanMessage(content=input))
        st.session_state.input = input

        output_container = st.empty()
        output_container = output_container.container(border=True)
        output_container.chat_message(name="Human:", avatar="🧑").write(input)
        # with st.chat_message(name="Human:", avatar="🧑"):
        #     st.write(input)

        answer_container = output_container.chat_message("assistant", avatar="🦜")

        asyncio.run(run_graph(answer_container))

    st.sidebar.write(st.session_state)






async def run_graph(answer_container):
    # with bot_reply_placeholder.chat_message("AI:", avatar="🤖"):
        # st.write("hi")

    # def print_callback(x):
    #     with bot_reply_placeholder.chat_message("AI:", avatar="🤖"):
    #         st.write(x)




    graph_config = RunnableConfig()
    st_callback = StreamlitCallbackHandler(answer_container)
    graph_config['callback'] = [st_callback]
    graph_config['hyperparameters'] = st.session_state.graph_hyperparameters
    graph_config['metadata'] = {
            "conversation_id": st.session_state.session_id
        }

    graph_input = {"input": st.session_state.input, "messages": st.session_state.convo_history}

    graph = build_graph(use_open_routing=False)


    # for node, output in get('construct').invoke(str(st.session_state.appstate.chat.messages)):
    async for event in graph.astream_events(
                            input=graph_input,
                            config=graph_config,
                            version='v1'
                        ):
        # st.json(event)
        pass
