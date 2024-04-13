from langchain.callbacks.base import BaseCallbackHandler

# from langchain_community.chat_message_histories import StreamlitChatMessageHistory
# from langchain_community.callbacks import StreamlitCallbackHandler
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# # from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage

import streamlit as st




class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        with self.container.chat_message("ai", avatar="🤖"):
            st.markdown(self.text)








def run_prompt(user_prompt_placeholder, bot_reply_placeholder):
    user_prompt_placeholder.chat_message("human", avatar="🗣️").write(st.session_state.prompt)

    ret = st.session_state.construct.run_prompt(bot_reply_placeholder)

    with bot_reply_placeholder:
        st.chat_message("ai", avatar="🤖").write(ret.content)







def cmp_convo_history():
    st.header("🗣️💬 :rainbow[Conversation history]", divider="rainbow")

    with st.container(height=500, border=True):
        for msg in st.session_state.langchain_messages:
            st.chat_message(msg.type, avatar="🗣️" if type(msg) is HumanMessage else "🤖").write(msg.content)
        user_prompt_placeholder = st.empty()
        bot_reply_placeholder = st.empty()

    st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))
