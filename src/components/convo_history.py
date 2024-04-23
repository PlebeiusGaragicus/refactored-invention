import asyncio
import inspect

from langchain.callbacks.base import BaseCallbackHandler

# from langchain_community.chat_message_histories import StreamlitChatMessageHistory
# from langchain_community.callbacks import StreamlitCallbackHandler
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# # from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage


import streamlit as st


from src.common import BOT_AVATAR, HUMAN_AVATAR


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        # with self.container.chat_message("ai", avatar="🤖"):
        with self.container.chat_message("ai", avatar=BOT_AVATAR):
            st.markdown(self.text)








def run_prompt(user_prompt_placeholder, bot_reply_placeholder, thoughts):
    user_prompt_placeholder.chat_message("human", avatar=HUMAN_AVATAR).write(st.session_state.prompt)

    ret = st.session_state.construct.run_prompt(bot_reply_placeholder, thoughts)

    with bot_reply_placeholder:
        # st.chat_message("ai", avatar="🤖").write(ret.content)
        with st.chat_message("ai", avatar=BOT_AVATAR):
            # if it's a generator
            # if type(ret.content) is not itertools.iterable:
            if inspect.isasyncgen(ret):
                async def write_async():
                    async for msg in ret:
                        st.write(msg)

                asyncio.run(write_async())
            else:
                st.write(ret.content)


def cmp_convo_thoughts():
    st.header("🧠 :blue[Thought Process]", divider="rainbow", anchor="thoughts")

    thought_container = st.empty()
    thought_container.container(height=500, border=True)
    # with st.container(height=500, border=True):
        # pass

    return thought_container





def cmp_convo_history(thoughts):
    st.header("🗣️💬 :rainbow[Conversation history]", divider="rainbow", anchor="ConvoHistory")

    with st.container(height=500, border=True):
        for msg in st.session_state.langchain_messages:
            st.chat_message(msg.type, avatar=HUMAN_AVATAR if type(msg) is HumanMessage else BOT_AVATAR).write(msg.content)
        user_prompt_placeholder = st.empty()
        bot_reply_placeholder = st.empty()

    st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder, thoughts,))




"""

{
"generate":"AIMessage(content='"The Little Prince," written by Antoine de Saint-Exupéry, remains relevant in modern life due to its timeless messages about love, friendship, and the importance of seeing beyond the surface. The story follows a young prince who travels to different planets and learns valuable lessons from his encounters with various characters. \n\nIn today\'s fast-paced world, where materialism and superficiality often dominate, the book\'s emphasis on cherishing the intangible qualities of life is more important than ever. The Little Prince reminds readers to look with their hearts, to appreciate the beauty of simplicity, and to nurture meaningful relationships. \n\nMoreover, the book\'s exploration of adult perspectives versus childlike innocence serves as a poignant reminder to maintain a sense of wonder and imagination in our lives. In a society consumed by productivity and efficiency, "The Little Prince" encourages us to slow down, reflect on what truly matters, and connect with our inner child.\n\nOverall, the enduring relevance of "The Little Prince" lies in its ability to inspire readers to cultivate empathy, compassion, and a deeper understanding of the world around them, making it a cherished classic with a message that resonates across generations.', response_metadata={'finish_reason': 'stop'}, id='run-eaa22285-4bd0-4143-8c14-7f2ae8818f62-0')"
}


{
"reflect":"HumanMessage(content='Your essay provides a concise overview of the enduring relevance of "The Little Prince" and its message in modern life. To strengthen your submission, consider expanding on the following points:\n\n1. **In-depth Analysis**: Delve deeper into specific examples from the book that highlight its messages on love, friendship, and looking beyond the surface. Explore how these themes manifest in today\'s society and offer real-world examples to support your points.\n\n2. **Contemporary Relevance**: Connect the themes of "The Little Prince" to current events or societal trends to emphasize its continued importance in addressing modern challenges or issues. This could add a layer of complexity to your argument.\n\n3. **Critical Thinking**: Challenge the reader to reflect on how they can personally apply the book\'s messages to their own lives. Encourage introspection and self-assessment in light of the themes presented in "The Little Prince."\n\n4. **Writing Style**: Ensure that your essay flows smoothly and transitions seamlessly between ideas. Consider varying your sentence structure to maintain reader engagement and interest.\n\nBy incorporating these suggestions, you can enrich your essay and provide a more comprehensive exploration of the topicality of "The Little Prince" in modern life. Remember to maintain a balance between analysis and personal reflection to create a compelling and thought-provoking piece.', id='6dcd7587-b2a7-473e-a1d4-e8a77a4173d3')"
}


"""