import asyncio
import inspect

from langchain_core.messages import HumanMessage

import streamlit as st

from src.common import BOT_AVATAR, HUMAN_AVATAR








import uuid
import asyncio

import streamlit as st

from langchain_community.callbacks import StreamlitCallbackHandler
# from streamlit.external.langchain import (StreamlitCallbackHandler as OfficialStreamlitCallbackHandler)
from langchain_core.callbacks import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from streamlit.runtime.scriptrunner import get_script_run_ctx

from langchain_community.callbacks.streamlit.mutable_expander import MutableExpander

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from src.interface import Colors, color, reset_color, cprint, cput, change_color, build_interface

import logging












#####################################################################################
#
#
#
#
#
#####################################################################################


def cmp_metrics():
    # st.header("📊 :blue[Metrics]", divider="rainbow")

    with st.container(border=True):
        st.text_input(":green[Session ID]", value=st.session_state.session_id, disabled=True)
        tokens = sum([len(msg.content) for msg in st.session_state.convo_history])
        st.text_input(":green[Tokens]", value=tokens, disabled=True)

        if len(st.session_state.convo_history) > 0:
            with st.popover("Graph state"): # Message json
                st.json(st.session_state.convo_history)


def cmp_convo_thoughts():
    st.header("🧠 :blue[Thought Process]", divider="rainbow", anchor="thoughts")

    thought_container = st.empty()
    thought_container.container(height=450, border=True)
    # with st.container(height=500, border=True):
        # pass

    return thought_container


def cmp_convo_history(thoughts):
    st.header("🗣️💬 :rainbow[Conversation history]", divider="rainbow", anchor="ConvoHistory")

    with st.container(height=500, border=True):
        for msg in st.session_state.convo_history:
            st.chat_message(msg.type, avatar=HUMAN_AVATAR if type(msg) is HumanMessage else BOT_AVATAR).write(msg.content)
        user_prompt_placeholder = st.empty()
        bot_reply_placeholder = st.empty()

    st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_graph, args=(user_prompt_placeholder, bot_reply_placeholder, thoughts,))

    cols3 = st.columns((1, 2, 1))
    with cols3[2]:
        st.button("🌱 :green[New]", use_container_width=True)


def cmp_bottom():

    bcol2 = st.columns((3, 2))
    with bcol2[1]:
        thoughts = cmp_convo_thoughts()
        cmp_metrics()


    with bcol2[0]:
        cmp_convo_history(thoughts)



    cols = st.columns((2, 1))
    with cols[1]:
        st.header(body="Thought Process", divider="rainbow")
        right = st.empty()
        # rc = right.popover("Thought Process")
        rc = right.container(border=True, height=600)
        status = rc.empty()
        # status = status.status("Running the graph", expanded=False, state="running")
        # status = MutableExpander("Running the graph", expanded=False, state="running")
        # rc.markdown("---")

        # st.spinner


    with cols[0]:
        st.header(body="Conversation History", divider="rainbow")
        left = st.empty()
        lc = left.container(border=True, height=600)

        for message in st.session_state.convo_history:
            with lc.chat_message(name=message.type):
                st.write(message.content)

    # with lc:
        if input := st.chat_input(placeholder="Question:", key="input"):
            # st.session_state.convo_history.append(HumanMessage(content=input))

            # with status.container():
            status_expander = status.status(":orange[Running:]", expanded=False, state="running")
            # with status.container():
            # status_expander.write('hi')


            with lc:
                st.chat_message(name="human").write(input)
                bot_reply_chatmessage = st.chat_message("assistant")

            # with lc:
                cols = st.columns((1, 1, 1))
                with cols[-1]:
                    interrupt_button = st.empty()
                # if interrupt_button.button("Interrupt", key="interrupt", on_click=lambda: st.rerun):
                if interrupt_button.button(":red[Interrupt]", key="interrupt", use_container_width=True):
                    # remove last item in convo_history
                    # del st.session_state.convo_history[-1]
                    # st.session_state.convo_history = st.session_state.convo_history[:-1]
                    # st.write(st.session_state.convo_history)
                    # print(st.session_state.convo_history)
                    st.rerun()

                with cols[0]:
                    with st.spinner("Thinking..."):
                        # status = st.empty()
                        # status.warning("Running the graph...")
                        asyncio.run(run_graph(rc, bot_reply_chatmessage, status_expander))
                        # status.empty()
                        # status.success("Done!")
                        status_expander.update(label=":green[Graph run complete]", state="complete")
                        # rc.success("Done!")
                        interrupt_button.empty()





















#####################################################################################
#
#                   THIS IS THE CODE THAT DOESN'T WORK
#
#                   THIS CODE IS RUN BY THE INTERFACE, ABOVE
#
#####################################################################################


async def run_graph(thought_container, bot_reply_chatmessage, status_expander):

    # st.info("Running the graph...")

    graph_config = RunnableConfig()
    # st_callback = StreamlitCallbackHandler(answer_container)
    # st_callback = custom_callback(answer_container)
    # st_callback = custom_callback()
    # st_callback = MyCustomHandler()
    # st_callback = StreamlitCallbackHandler(st.container())
    # graph_config['callbacks'] = [st_callback]
    # graph_config['callbacks'] = [StreamingStdOutCallbackHandler()]
    # graph_config['callbacks'] = [callback()]
    graph_config['hyperparameters'] = st.session_state.graph_hyperparameters
    graph_config['metadata'] = {"conversation_id": st.session_state.session_id}
    st.sidebar.markdown("# Graph config:")
    st.sidebar.json(graph_config)

    graph_input = {"input": st.session_state.input, "messages": st.session_state.convo_history}
    st.sidebar.markdown("# Graph input:")
    st.sidebar.json(graph_input)

    # NOTE: we give parameters to the graph builder as it will be used to differentiate builds of the graph!!
    graph = build_graph(use_open_routing=False)




    # on_chat_model_stream




    streamed_chunks = ""
    current_node = None
    # current_writer = None
    current_writer = bot_reply_chatmessage.empty()
    thought_writer = None
    async for event in graph.astream_events(
                            input=graph_input,
                            config=graph_config,
                            version='v1'
                        ):
        print(event)
        print('\n\n')
        # thought_text.json(event)
        status_expander.write(event['event'])
        status_expander.update(label=f":orange[Running:] :red[{event['event']}]")

        if event['event'] == "on_chain_end":
            if event['name'] == "LangGraph":
                last_node = event['data']['output'].keys()
                # print(last_node)
                # get the first key
                last_key = list(last_node)[0]
                last_message = event['data']['output'].get(last_key)['messages'][0].content

        if event['event'] != current_node:
            streamed_chunks = ""
            current_node = event['event']
            # thought_container.write(f"Node: {current_node}")

            if current_node not in ["on_chat_model_stream", "on_llm_new_token"]:
                continue

            # current_thought = thought_container.status(f"{current_node}", state="running", expanded=True)
            # with current_thought:
                # thought_writer = st.empty()
            # if thought_writer:
                # thought_writer.markdown("\n---\n")
            thought_writer = thought_container.empty()
            # thought_writer = thought_writer.container()
            # thought_writer.markdown("\n---\n")
            # thought_writer.write(f"Node: {current_node}")


        # feedback_type = event['metadata'].get('feedback_type', None)
        feedback_type = event['metadata'].get('UI_name', None)

        # AN LLM IS GIVING FEEDBACK TO THE USER!
        if feedback_type == "Friendly Chatbot":
            if event['data'].get('chunk', None):
                streamed_chunks += event['data']['chunk'].content
                current_writer.markdown(streamed_chunks)

                # with current_writer:
                    # st.write(streamed_chunks)
                    # current_writer.update()


        if feedback_type == "Ollama Router":
            if event['data'].get('chunk', None):
                streamed_chunks += event['data']['chunk'].content
                thought_writer.code(streamed_chunks)

    st.session_state.convo_history.append(HumanMessage(content=st.session_state.input))
    st.session_state.convo_history.append(AIMessage(content=last_message))









# def run_prompt(user_prompt_placeholder, bot_reply_placeholder, thoughts):
#     user_prompt_placeholder.chat_message("human", avatar=HUMAN_AVATAR).write(st.session_state.prompt)

#     ret = st.session_state.construct.run_prompt(bot_reply_placeholder, thoughts)

#     with bot_reply_placeholder:
#         # st.chat_message("ai", avatar="🤖").write(ret.content)
#         with st.chat_message("ai", avatar=BOT_AVATAR):
#             # if it's a generator
#             # if type(ret.content) is not itertools.iterable:
#             if inspect.isasyncgen(ret):
#                 async def write_async():
#                     async for msg in ret:
#                         st.write(msg)

#                 asyncio.run(write_async())
#             else:
#                 st.write(ret.content)

