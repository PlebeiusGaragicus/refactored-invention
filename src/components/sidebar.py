import uuid

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st

from src.constructs import ALL_CONSTRUCTS
from src.interface import center_text


def cmp_constructs():
    construct_names = [c.name for c in ALL_CONSTRUCTS]

    if "selected_construct" not in st.session_state:
        st.session_state.selected_construct = None
        st.toast("Welcome to PlebChat!", icon="🎉")

    # selected = st.radio("Construct", ["Ollama", "OpenAI"], key="chosen_construct", horizontal=True, index=0, label_visibility="collapsed")
    selected = st.radio("Construct", construct_names, horizontal=True, index=0, label_visibility="collapsed")

    if selected == st.session_state.selected_construct:
        return

    st.session_state.selected_construct = selected

    for Construct in ALL_CONSTRUCTS:
        if Construct.name == selected:
            st.session_state["construct"] = Construct()

    st.toast(f"Switched to {selected}!", icon=st.session_state["construct"].avatar)

    new_chat()
    # st.rerun()



def new_chat():
    # Note: new messages are saved to history automatically by Langchain during run
    # https://api.python.langchain.com/en/latest/chat_message_histories/langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory.html
    # if "msgs" in st.session_state:
        # del st.session_state.msgs
    st.session_state.msgs = StreamlitChatMessageHistory(key="langchain_messages")
    st.session_state.msgs.clear()
    st.session_state.session_id = uuid.uuid4()
    # st.write(st.session_state.session_id)




def draw_clear_button(container):
    with container:
        # if len(st.session_state.langchain_messages) > 0:
            # st.button("🗑️ :red[Clear messages]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True)

        clz2 = st.columns((1, 1))
        with clz2[0]:
            # st.button("🌱 :green[New]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))
            st.button("🗑️ :red[Clear]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))
        with clz2[1]:
            st.button("💾 :blue[Save]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))



def cmp_saved_conversations():
    st.header("", divider="rainbow")
    st.markdown("# :blue[Saved Conversations]")
    # st.markdown(".")
    if len(st.session_state.langchain_messages) > 0:
        clear_button_placeholder = st.empty()
        draw_clear_button(clear_button_placeholder)
        center_text("p", "---", 7)

    #TODO - implement saved conversations
    st.button("[None saved yet]", use_container_width=True, disabled=True)



def draw_messages():
    with st.expander("Debug", expanded=False):
        st.write(st.session_state)
        st.write(st.session_state.construct)

    # st.markdown(st.session_state.msgs) # class 'langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory
    # st.markdown(type(st.session_state.langchain_messages)) # list




def cmp_debug():
    st.header("", divider="rainbow")
    st.markdown("#")
    draw_messages()
    if len(st.session_state.langchain_messages) > 0:
        with st.popover("Graph state"): # Message json
            st.json(st.session_state.langchain_messages)
