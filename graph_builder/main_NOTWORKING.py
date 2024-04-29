import os
import uuid
import dotenv
import asyncio


import streamlit as st

# from langchain_community.callbacks import StreamlitCallbackHandler
from streamlit.external.langchain import (StreamlitCallbackHandler as OfficialStreamlitCallbackHandler)
from langchain_core.callbacks import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
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
        # with answer_container:
            # bot_reply_placeholder = st.empty()
        # answer_container = output_container.container(border=True)

        asyncio.run(run_graph(answer_container))
        # run_graph(answer_container)

    st.sidebar.write(st.session_state)

































"""Implements with_streamlit_context.

Created by Wessel Valkenburg, 2024-03-27.
"""
import threading
from typing import Any, TypeVar, cast

from streamlit.errors import NoSessionContext
from streamlit.runtime.scriptrunner.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
    get_script_run_ctx,
)

T = TypeVar("T")


def with_streamlit_context(fn: T) -> T:
    """Fix bug in streamlit which raises streamlit.errors.NoSessionContext."""
    ctx = get_script_run_ctx()

    if ctx is None:
        raise NoSessionContext(
            "with_streamlit_context must be called inside a context; "
            "construct your function on the fly, not earlier."
        )

    def _cb(*args: Any, **kwargs: Any) -> Any:
        """Do it."""

        thread = threading.current_thread()
        do_nothing = hasattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME) and (
            getattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME) == ctx
        )

        if not do_nothing:
            setattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME, ctx)

        # Call the callback.
        ret = fn(*args, **kwargs)

        if not do_nothing:
            # Why delattr? Because tasks for different users may be done by
            # the same thread at different times. Danger danger.
            delattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME)
        return ret

    return cast(T, _cb)











# class callback(BaseCallbackHandler):
#     def on_llm_start(self, serialized, prompts, **kwargs):
#         pass

#     def on_chat_model_start(self, serialized, messages, **kwargs):
#         pass

#     @with_streamlit_context
#     def on_llm_new_token(self, token, **kwargs):
#         print(token, end='', flush=True)
#         st.write(token)

#     def on_llm_end(self, response, **kwargs):
#         pass

#     def on_llm_error(self, error, **kwargs):
#         pass

#     def on_chain_start(self, serialized, inputs, **kwargs):
#         pass

#     def on_chain_end(self, outputs, **kwargs):
#         pass

#     def on_chain_error(self, error, **kwargs):
#         pass

#     def on_tool_start(self, serialized, input_str, **kwargs):
#         pass

#     def on_agent_action(self, action, **kwargs):
#         pass

#     def on_tool_end(self, output, **kwargs):
#         pass

#     def on_tool_error(self, error, **kwargs):
#         pass



class custom_callback(OfficialStreamlitCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = "will it work?"):
        self.container = container
        self.text = initial_text

    @with_streamlit_context
    def on_llm_new_token(self, token, **kwargs):
        # print(token, end='', flush=True)
        self.text += token
        self.container.markdown(self.text)
    
    @with_streamlit_context
    def on_chat_model_stream(self, token, **kwargs):
        # print(token, end='', flush=True)
        self.text += token
        self.container.markdown(self.text)



async def run_graph(answer_container):
# def run_graph(answer_container):
    # with bot_reply_placeholder.chat_message("AI:", avatar="🤖"):
        # st.write("hi")

    # def print_callback(x):
    #     with bot_reply_placeholder.chat_message("AI:", avatar="🤖"):
    #         st.write(x)

    answer_container.markdown("answer goes here")


    from streamlit.runtime.scriptrunner import get_script_run_ctx


    graph_config = RunnableConfig()
    # st_callback = StreamlitCallbackHandler(answer_container)
    st_callback = custom_callback(answer_container)
    # st_callback = custom_callback()
    # st_callback = StreamlitCallbackHandler(st.container())
    graph_config['callbacks'] = [st_callback]
    # graph_config['callbacks'] = [StreamingStdOutCallbackHandler(), callbak]
    # graph_config['callbacks'] = [callback()]
    graph_config['hyperparameters'] = st.session_state.graph_hyperparameters
    graph_config['metadata'] = {
            "conversation_id": st.session_state.session_id
        }

    graph_input = {"input": st.session_state.input, "messages": st.session_state.convo_history}

    graph = build_graph(use_open_routing=False)

    st.sidebar.json(graph_config)

    # for node, output in get('construct').invoke(str(st.session_state.appstate.chat.messages)):
    async for event in graph.astream_events(
    # for node in graph.invoke(
                            input=graph_input,
                            config=graph_config,
                            version='v1'
                        ):

        print(event['event'], event['name'])
        # st.title(node)
        # st.write(output)
        # with st.status(f"{event['event']} : {event['name']}", expanded=False, state="complete"):
            # st.json(event)
        pass
