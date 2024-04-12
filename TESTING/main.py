import dotenv
import os
import uuid

from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st

import TESTING.constructs.chain_ollama as chain_ollama
from TESTING.constructs import ALL_CONSTRUCTS

# https://github.com/langchain-ai/streamlit-agent


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        with self.container.chat_message("ai", avatar="🤖"):
            st.markdown(self.text)


def draw_messages(view_messages):
    with view_messages:
        st.json(st.session_state.langchain_messages)
        st.write(st.session_state)
        st.write(st.session_state.construct)
        # st.markdown(st.session_state.msgs) # class 'langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory
        # st.markdown(type(st.session_state.langchain_messages)) # list



def draw_clear_button(container):
    with container:
        if len(st.session_state.langchain_messages) > 0:
            st.button(":red[Clear messages]", on_click=lambda: st.session_state.langchain_messages.clear())



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
    # if "msgs" in st.session_state:
        # del st.session_state.msgs
    st.session_state.msgs = StreamlitChatMessageHistory(key="langchain_messages")
    st.session_state.msgs.clear()
    st.session_state.session_id = uuid.uuid4()
    st.sidebar.write(st.session_state.session_id)


def run_prompt(user_prompt_placeholder, bot_reply_placeholder):
    user_prompt_placeholder.chat_message("human", avatar="🗣️").write(st.session_state.prompt)

    ret = st.session_state.construct.run_prompt(bot_reply_placeholder)

    with bot_reply_placeholder:
        st.chat_message("ai", avatar="🤖").write(ret.content)


def main():
    dotenv.load_dotenv()
    st.set_page_config(page_title="LangChain intergration testing", page_icon="📖", layout="wide")
    st.title("📖 LangChain intergration testing")

    cmp_constructs()

    with st.popover(":blue[Settings]"):
        st.session_state["construct"].show_settings()

    st.header("", divider="rainbow")

    # Note: new messages are saved to history automatically by Langchain during run
    # https://api.python.langchain.com/en/latest/chat_message_histories/langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory.html
    if "langchain_messages" not in st.session_state:
        new_chat()


    # view_messages = st.sidebar.popover(":red[debug]")
    view_messages = st.sidebar.container(border=True)

    for msg in st.session_state.langchain_messages:
        st.chat_message(msg.type, avatar="🗣️" if type(msg) is HumanMessage else "🤖").write(msg.content)

    user_prompt_placeholder = st.empty()
    bot_reply_placeholder = st.empty()
    clear_button_placeholder = st.empty()

    st.chat_input("Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))
    # run_prompt(bot_reply_placeholder)

    draw_clear_button(clear_button_placeholder)
    draw_messages(view_messages)











# def run_prompt(prompt, bot_reply_placeholder):
#     llm_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", "You are an human having an informal conversation with a friend. Your reply should be very short."),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{question}"),
#         ]
#     )

#     config = {"configurable": {"session_id": "any"}}

#     # stream_handler = StreamHandler(bot_reply_placeholder)
#     stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
#     llm = ChatOllama(model="mistral:7b", streaming=True, callbacks=[stream_handler])
#     chain = llm_prompt | llm

#     construct = RunnableWithMessageHistory(
#         chain,
#         lambda session_id: st.session_state.msgs,
#         input_messages_key="question",
#         history_messages_key="history",
#     )

#     return construct.invoke({"question": prompt}, config)


# def interrupt():
#     st.chat_message("human", avatar="🗣️").write("Hold on - let me interrupt you...")
