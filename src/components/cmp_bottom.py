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


def cmp_metrics(container):
    # st.header("📊 :blue[Metrics]", divider="rainbow")

    # with st.container(border=True):
    with container.container(border=True):
        st.text_input(":green[Session ID]", value=st.session_state.session_id, disabled=True)

        cols2 = st.columns((1, 1))
        with cols2[1]:
            tokens = sum([len(msg.content) for msg in st.session_state.convo_history])
            # st.text_input(":green[Tokens]", value=tokens, disabled=True)
            st.write(f":green[Tokens:] :orange[{tokens}]")

        with cols2[0]:
            # if len(st.session_state.convo_history) > 0:
            with st.popover("Convo history", use_container_width=True): # Message json
                st.json(st.session_state.convo_history)
            
            with st.popover("hyperparameters", use_container_width=True):
                st.json(st.session_state.graph_hyperparameters)

            with st.popover("session state", use_container_width=True):
                st.json(st.session_state)


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

    # cols3 = st.columns((2, 1, 1))
    # with cols3[0]:
    #     # st.button("nothing", use_container_width=True)
    #     # pass
    #     with st.container(border=True):
    #         tokens = sum([len(msg.content) for msg in st.session_state.convo_history])
    #         st.write(f":green[Tokens:] `{tokens}`")

    # if len(st.session_state.convo_history) > 0:
    #     with cols3[1]:
    #         if 'saved' in st.session_state:
    #             with st.popover(":red[Delete thread]", use_container_width=True):
    #                 st.warning("Are you sure?!")
    #                 if st.button("🗑️ :red[Delete]", use_container_width=True):
    #                     # import time
    #                     st.toast("NOT YET IMPLEMENTED")
    #                     # time.sleep(1)

    #         else:
    #             if st.button("💾 :blue[Save thread]", use_container_width=True):
    #                 st.toast("NOT YET IMPLEMENTED")

    # with cols3[2]:
    #     if st.button("🌱 :green[New]", use_container_width=True):
    #         st.toast("NOT YET IMPLEMENTED")







def cmp_buttons():
    cols3 = st.columns((2, 1, 1))
    with cols3[0]:
        pass
        # with st.container(border=True):
        #     tokens = sum([len(msg.content) for msg in st.session_state.convo_history])
        #     st.write(f":green[Tokens:] `{tokens}`")

    if len(st.session_state.convo_history) > 0:
        with cols3[1]:
            if 'saved' in st.session_state:
                with st.popover(":red[Delete thread]", use_container_width=True):
                    st.warning("Are you sure?!")
                    if st.button("🗑️ :red[Delete]", use_container_width=True):
                        st.toast("NOT YET IMPLEMENTED")

            else:
                if st.button("💾 :blue[Save thread]", use_container_width=True):
                    st.toast("NOT YET IMPLEMENTED")

    with cols3[2]:
        if st.button("🌱 :green[New]", use_container_width=True):
            st.toast("NOT YET IMPLEMENTED")






def cmp_bottom():
    cols = st.columns((3, 2))
    with cols[1]:
        st.header("🧠 :blue[Thought Process]", divider="rainbow", anchor="thoughts")
        right = st.empty()
        rc = right.container(border=True, height=550)
        status = rc.empty()

        metrics_container = st.empty()
        # cmp_metrics(metrics_container)



    with cols[0]:
        st.header("🗣️💬 :rainbow[Conversation history]", divider="rainbow", anchor="ConvoHistory")
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

                        error = None
                        try:
                            asyncio.run(st.session_state.construct.run_graph(rc, bot_reply_chatmessage, status_expander))
                        except Exception as e:
                            error = e

                        interrupt_button.empty()
                        if error:
                            status_expander.update(label=":red[Graph run failed]", state="error")
                            # status_expander.update(label=":red[Graph run failed]", state="error", expanded=True)
                            # status_expander.write(f"Error: {error}")
                            bot_reply_chatmessage.error(f"Error: {error}")
                            import traceback
                            bot_reply_chatmessage.code('\n'.join(traceback.format_exception(None, error, error.__traceback__)))
                            # tb = "Traceback:\n" + '\n'.join(traceback.format_exception(None, error, error.__traceback__))
                            # with st.popover("traceback"):
                                # bot_reply_chatmessage.code(tb)
                            interrupt_button.empty()
                        else:
                            status_expander.update(label=":green[Graph run complete]", state="complete")

                        # rc.success("Done!")


        cmp_buttons()

        metrics_container.empty()
        cmp_metrics(metrics_container)
