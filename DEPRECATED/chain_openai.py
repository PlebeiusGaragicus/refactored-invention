import os
from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

import streamlit as st

from src.components.presets import find_preset



# OPENAI_MODELS = ["gpt-3.5-turbo-1106"]
# https://platform.openai.com/docs/models/gpt-3-5-turbo
# TODO - too many choices... also, should I provide pricing/info for each model...? model info card?
OPENAI_MODELS = [
        # "gpt-4-0125-preview",
        "gpt-4-turbo-preview",
        # "gpt-4-1106-preview",
        # "gpt-4-vision-preview",
        "gpt-4",
        # "gpt-4-0314",
        # "gpt-4-0613",
        # "gpt-4-32k",
        # "gpt-4-32k-0314",
        # "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        # "gpt-3.5-turbo-16k",
        # "gpt-3.5-turbo-0301",
        # "gpt-3.5-turbo-0613",
        # "gpt-3.5-turbo-1106",
        # "gpt-3.5-turbo-0125",
        # "gpt-3.5-turbo-16k-0613",
    ]

DEFAULT_SYSTEM_PROMPT = """You are an human having an informal conversation with a friend. Your reply should be very short."""

class OpenAIChain():
    name: str = "OpenAI"
    avatar: str = "💫"

    def show_prompts(self):
        st.text_area("System Prompt",
                height=200,
                value=find_preset("system_prompt", default=DEFAULT_SYSTEM_PROMPT),
                key="preset_system_prompt")


    def show_settings(self):
        # options = ["dolphin-mistral:latest", "mistral:7b", "llama2:7b", "gemma:2b"]
        # st.selectbox(label="Model", options=options,
        #         index=find_preset("selected_model", is_index=True, options_list=options, default=0),
        #         key="preset_selected_model",)
        st.selectbox("Model", OPENAI_MODELS,
                index=find_preset("selected_model", is_index=True, options_list=OPENAI_MODELS, default=0),
                key="preset_selected_model")
        st.slider(label="Temperature",
                min_value=0.0, max_value=1.0, step=0.01,
                value=find_preset("temperature", default=0.5),
                key="preset_temperature")


    def run_prompt(self, bot_reply_placeholder):
        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", st.session_state.preset_system_prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{user_prompt}"),
            ]
        )

        config = {"configurable": {"session_id": str(st.session_state.session_id)}}

        stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        llm = ChatOpenAI(
                model=st.session_state.preset_selected_model,
                temperature=st.session_state.preset_temperature,
                api_key=api_key,
                streaming=True,
                callbacks=[stream_handler]
            )

        chain = llm_prompt | llm

        construct = RunnableWithMessageHistory(
            chain,
            lambda session_id: st.session_state.msgs,
            input_messages_key="user_prompt",
            history_messages_key="history",
        )

        print(construct)
        # st.sidebar.write(construct)

        return construct.invoke({"user_prompt": st.session_state.prompt}, config)