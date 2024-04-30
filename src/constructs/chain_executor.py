import os
import asyncio
from pathlib import Path


from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.chains import LLMMathChain
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.callbacks import StreamlitCallbackHandler

from langchain_community.chat_models import ChatOllama

from typing import List, Sequence

from langgraph.graph import END, MessageGraph

from pydantic import BaseModel

import streamlit as st

# from src.components.presets import find_preset






# OPENAI_MODELS = ["gpt-3.5-turbo-1106"]
# https://platform.openai.com/docs/models/gpt-3-5-turbo
# TODO - too many choices... also, should I provide pricing/info for each model...? model info card?
MODELS = ["..."]

DEFAULT_SYSTEM_PROMPT = """You are an human having an informal conversation with a friend. Your reply should be very short."""

class ToolsAgent():
    name: str = "ToolsAgent"
    avatar: str = "🛠️"

    def show_prompts(self):
        pass
        # st.text_area("System Prompt",
        #         height=200,
        #         value=find_preset("system_prompt", default=DEFAULT_SYSTEM_PROMPT),
        #         key="preset_system_prompt")


    def show_settings(self):
        pass
        # st.warning("nothing yet...")


    def run_prompt(self, bot_reply_placeholder, thoughts):
        # llm_prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", st.session_state.preset_system_prompt),
        #         MessagesPlaceholder(variable_name="history"),
        #         ("human", "{user_prompt}"),
        #     ]
        # )

        # config = {"configurable": {"session_id": str(st.session_state.session_id)}}

        # stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)

        # llm = ChatOpenAI(
        #         model=st.session_state.preset_selected_model,
        #         temperature=st.session_state.preset_temperature,
        #         streaming=True,
        #         callbacks=[stream_handler]
        #     )

        # chain = llm_prompt | llm

        # construct = RunnableWithMessageHistory(
        #     chain,
        #     lambda session_id: st.session_state.msgs,
        #     input_messages_key="user_prompt",
        #     history_messages_key="history",
        # )

        # print(construct)

        # return construct.invoke({"user_prompt": st.session_state.prompt}, config)





        # Tools setup
        from langchain_experimental.llms.ollama_functions import OllamaFunctions

        llm = OllamaFunctions(model="mistral", api_key=os.getenv("MISTRAL_API_KEY"))
        llm_math_chain = LLMMathChain.from_llm(llm)


        tools = [
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="useful for when you need to answer questions about math",
            ),
        ]

        # Initialize agent
        react_agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
        mrkl = AgentExecutor(agent=react_agent, tools=tools)

        output_container = st.empty()
        output_container = output_container.container()
        output_container.chat_message("user").write(st.session_state.prompt)

        answer_container = output_container.chat_message("assistant", avatar="🦜")
        st_callback = StreamlitCallbackHandler(answer_container)
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_callback]

        answer = mrkl.invoke({"input": st.session_state.prompt}, cfg)

        answer_container.write(answer["output"])

