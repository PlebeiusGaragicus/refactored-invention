# from langchain.memory import ChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory

# demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

# chain_with_message_history = RunnableWithMessageHistory(
#     chain,
#     lambda session_id: demo_ephemeral_chat_history_for_chain,
#     input_messages_key="input",
#     history_messages_key="chat_history",
# )

import streamlit as st



# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# # from langchain_openai.chat_models import ChatOpenAI

# from langchain_community.chat_models import ChatOllama
# from langchain_community.llms import Ollama

# # model = ChatOpenAI()
# model = ChatOllama

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You're an assistant who's good at {ability}. Respond in 20 words or fewer",
#         ),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}"),
#     ]
# )
# runnable = prompt | model


# for c in runnable.astream({
#         "input": "I'm good at playing the guitar"
#     }):
#     st.write(c["output"])



# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# supports many more optional parameters. Hover on your `ChatOllama(...)`
# class to view the latest available supported parameters
llm = ChatOllama(model="llama2")
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

# using LangChain Expressive Language chain syntax
# learn more about the LCEL on
# /docs/expression_language/why
chain = prompt | llm | StrOutputParser()

# chain.ainvoke({"topic": "Space travel"})




async def run():
    with st.spinner("Loading..."):
        # st.write(chain.ainvoke({"topic": "Space travel"}))

        async for c in chain.ainvoke({"topic": "Space travel"}):
            st.write(c["output"])

import asyncio


# for c in chain.ainvoke({
#         "input": "I'm good at playing the guitar"
#     }):
#     st.write(c["output"])
