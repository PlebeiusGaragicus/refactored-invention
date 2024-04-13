from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama

import streamlit as st

from TESTING.common import cprint, Colors

SYSTEM_PROMPT = """You are an human having an informal conversation with a friend.
Your reply should be very short. Don't be apologetic. Don't use proper syntax and punctuation.
Do no overuse emoji.  You are not `system.`
If I don't say much, don't try to fill in the conversation."""

REFLECTOR_PROMPT = """Just be chillin, bro!"""



class OllamaSimpleChain():
    name: str = "Ollama"
    avatar: str = "🦙"

    def show_prompts(self):
        st.text_area("SYSTEM", key="system_prompt", height=150, value=SYSTEM_PROMPT)
        st.text_area("Reflector Prompt", key="reflector_prompt", height=150, value=REFLECTOR_PROMPT)

    def show_settings(self):
        st.selectbox("Model", ["dolphin-mistral:latest", "mistral:7b", "llama2:7b", "gemma:2b"], key="selected_model")
        st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="temperature")
        # st.checkbox("Safe Mode", value=True, key="safe_mode")


    def run_prompt(self, bot_reply_placeholder):
        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", st.session_state.system_prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{user_prompt}"),
            ]
        )

        config = {"configurable": {"session_id": str(st.session_state.session_id)}}

        # stream_handler = StreamHandler(bot_reply_placeholder)
        stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
        llm = ChatOllama(
                model=st.session_state.selected_model,
                streaming=True,
                temperature=str(st.session_state.temperature),
                callbacks=[stream_handler]
            )
        chain = llm_prompt | llm

        construct = RunnableWithMessageHistory(
            chain,
            lambda session_id: st.session_state.msgs,
            input_messages_key="user_prompt",
            history_messages_key="history",
        )

        cprint("\n\nCONSTRUCT RUNNABLE:", Colors.YELLOW)
        cprint(str(construct), Colors.GREEN)

        return construct.invoke({"user_prompt": st.session_state.prompt}, config)