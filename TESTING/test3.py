import dotenv
import os

from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st


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
        """
        Message History initialized with:
        ```python
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        ```

        Contents of `st.session_state.langchain_messages`:
        """
        view_messages.json(st.session_state.langchain_messages)

        view_messages.markdown(st.session_state.msgs) # class 'langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory
        view_messages.markdown(type(st.session_state.langchain_messages)) # list



def run_prompt(prompt):
    st.chat_message("human", avatar="🗣️").write(prompt)

    llm_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI chatbot having an informal conversation with a human. Keep replies very brief"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    config = {"configurable": {"session_id": "any"}}

    # stream_handler = StreamHandler(st.empty())
    stream_handler = StreamHandler(st.empty())

    llm = ChatOllama(model="mistral:7b", streaming=True, callbacks=[stream_handler])
    chain = llm_prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: st.session_state.msgs,
        input_messages_key="question",
        history_messages_key="history",
    )

    response = chain_with_history.invoke({"question": prompt}, config)








if __name__ == "__main__":
    dotenv.load_dotenv()
    st.set_page_config(page_title="LangChain intergration testing", page_icon="📖")
    st.title("📖 LangChain intergration testing")


    # Note: new messages are saved to history automatically by Langchain during run
    if "langchain_messages" not in st.session_state:
        st.session_state.msgs = StreamlitChatMessageHistory(key="langchain_messages")
        # StreamlitChatMessageHistory(key="langchain_messages")
        # if len(msgs.messages) == 0:
        #     msgs.add_ai_message("How can I help you?")



    view_messages = st.popover("message history")

    for msg in st.session_state.langchain_messages:
        st.chat_message(msg.type, avatar="🗣️" if type(msg) is HumanMessage else "🤖").write(msg.content)

    if prompt := st.chat_input():
        run_prompt(prompt)

    draw_messages(view_messages)
