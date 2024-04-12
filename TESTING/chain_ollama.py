from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama

import streamlit as st



# class settings:
#     name: str = "Ollama"
#     version: str = "0.0.1"
#     models: list = ["mistral:7b", "llama2:7b"]

# class OllamaSimpleChain():
#     def __init__(self, model="mistral:7b"):
#         self.model = None



def show_settings():
    st.checkbox("Safe Mode", value=True, key="safe_mode")


def run_prompt(prompt, bot_reply_placeholder):
    llm_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an human having an informal conversation with a friend. Your reply should be very short."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    config = {"configurable": {"session_id": "any"}}

    # stream_handler = StreamHandler(bot_reply_placeholder)
    stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
    llm = ChatOllama(model="mistral:7b", streaming=True, callbacks=[stream_handler])
    chain = llm_prompt | llm

    construct = RunnableWithMessageHistory(
        chain,
        lambda session_id: st.session_state.msgs,
        input_messages_key="question",
        history_messages_key="history",
    )

    return construct.invoke({"question": prompt}, config)