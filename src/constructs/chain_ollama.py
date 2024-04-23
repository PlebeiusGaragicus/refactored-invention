from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama

import streamlit as st

from src.common import cprint, Colors
from src.components.presets import find_preset

SYSTEM_PROMPT = """You are an human having an informal conversation with a friend.
Your reply should be very short. Don't be apologetic. Don't use proper syntax and punctuation.
Do no overuse emoji.  You are not `system.`
If I don't say much, don't try to fill in the conversation."""

REFLECTOR_PROMPT = """Just be chillin, bro!"""



class OllamaSimpleChain():
    name: str = "Ollama"
    avatar: str = "🦙"

    def show_settings(self):
        options = ["dolphin-mistral:latest", "mistral:7b", "llama2:7b", "gemma:2b"]
        st.selectbox(label="Model", options=options,
                index=find_preset("selected_model", is_index=True, options_list=options, default=0),
                key="preset_selected_model")

        st.slider(label="Temperature",
                min_value=0.0, max_value=1.0, step=0.01,
                value=find_preset("temperature", default=0.5),
                key="preset_temperature")


    def show_prompts(self):
        st.text_area(label="SYSTEM PROMPT", height=150,
                    value=find_preset("system_prompt", default=SYSTEM_PROMPT),
                    key="preset_system_prompt")



    def run_prompt(self, bot_reply_placeholder):
        print(st.session_state.preset_system_prompt)
        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", st.session_state.preset_system_prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{user_prompt}"),
            ]
        )

        config = {"configurable": {"session_id": str(st.session_state.session_id)}}

        # stream_handler = StreamHandler(bot_reply_placeholder)
        thought_labeler = BaseCallbackHandler()
        stream_handler = StreamlitCallbackHandler(
                            bot_reply_placeholder,
                            collapse_completed_thoughts=True)#,
                            # thought_labeler=thought_labeler)

        llm = ChatOllama(
                model=st.session_state.preset_selected_model,
                streaming=True,
                temperature=str(st.session_state.preset_temperature),
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