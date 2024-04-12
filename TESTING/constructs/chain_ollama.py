from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama

import streamlit as st


class OllamaSimpleChain():
    name: str = "Ollama"
    avatar: str = "🦙"

    def show_settings(self):
        st.selectbox("Model", ["dolphin-mistral:latest", "mistral:7b", "llama2:7b", "gemma:2b"], key="selected_model")
        # st.checkbox("Safe Mode", value=True, key="safe_mode")


    def run_prompt(self, bot_reply_placeholder):
        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an human having an informal conversation with a friend. Your reply should be very short."),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{user_prompt}"),
            ]
        )

        config = {"configurable": {"session_id": str(st.session_state.session_id)}}

        # stream_handler = StreamHandler(bot_reply_placeholder)
        stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
        llm = ChatOllama(model=st.session_state.selected_model, streaming=True, callbacks=[stream_handler])
        chain = llm_prompt | llm

        construct = RunnableWithMessageHistory(
            chain,
            lambda session_id: st.session_state.msgs,
            input_messages_key="user_prompt",
            history_messages_key="history",
        )

        st.sidebar.write(construct)

        return construct.invoke({"user_prompt": st.session_state.prompt}, config)