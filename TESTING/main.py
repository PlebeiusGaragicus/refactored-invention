import dotenv
import os
import uuid

from langchain.callbacks.base import BaseCallbackHandler

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st

import TESTING.constructs.chain_ollama as chain_ollama
from TESTING.constructs import ALL_CONSTRUCTS

# https://github.com/langchain-ai/streamlit-agent


COL_HEIGHT = 550



# def run_prompt(prompt, bot_reply_placeholder):
#     llm_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", "You are an human having an informal conversation with a friend. Your reply should be very short."),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{question}"),
#         ]
#     )

#     config = {"configurable": {"session_id": "any"}}

#     # stream_handler = StreamHandler(bot_reply_placeholder)
#     stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
#     llm = ChatOllama(model="mistral:7b", streaming=True, callbacks=[stream_handler])
#     chain = llm_prompt | llm

#     construct = RunnableWithMessageHistory(
#         chain,
#         lambda session_id: st.session_state.msgs,
#         input_messages_key="question",
#         history_messages_key="history",
#     )

#     return construct.invoke({"question": prompt}, config)


# def interrupt():
#     st.chat_message("human", avatar="🗣️").write("Hold on - let me interrupt you...")



def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')



def center_text(type, text, size=None):
    if size == None:
        st.write(f"<{type} style='text-align: center;'>{text}</{type}>", unsafe_allow_html=True)
    else:
        st.write(f"<{type} style='text-align: center; font-size: {size}px;'>{text}</{type}>", unsafe_allow_html=True)













class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        with self.container.chat_message("ai", avatar="🤖"):
            st.markdown(self.text)


def draw_messages():
    with st.expander("Debug", expanded=False):
        st.write(st.session_state)
        st.write(st.session_state.construct)

    # st.markdown(st.session_state.msgs) # class 'langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory
    # st.markdown(type(st.session_state.langchain_messages)) # list



def draw_clear_button(container):
    with container:
        # if len(st.session_state.langchain_messages) > 0:
            # st.button("🗑️ :red[Clear messages]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True)

        st.button("🗑️ :red[Clear messages]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))


def cmp_constructs():
    construct_names = [c.name for c in ALL_CONSTRUCTS]

    if "selected_construct" not in st.session_state:
        st.session_state.selected_construct = None
        st.toast("Welcome to PlebChat!", icon="🎉")

    # selected = st.radio("Construct", ["Ollama", "OpenAI"], key="chosen_construct", horizontal=True, index=0, label_visibility="collapsed")
    selected = st.radio("Construct", construct_names, horizontal=True, index=0, label_visibility="collapsed")

    if selected == st.session_state.selected_construct:
        return

    st.session_state.selected_construct = selected

    for Construct in ALL_CONSTRUCTS:
        if Construct.name == selected:
            st.session_state["construct"] = Construct()

    st.toast(f"Switched to {selected}!", icon=st.session_state["construct"].avatar)

    new_chat()
    # st.rerun()



def new_chat():
    # Note: new messages are saved to history automatically by Langchain during run
    # https://api.python.langchain.com/en/latest/chat_message_histories/langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory.html
    # if "msgs" in st.session_state:
        # del st.session_state.msgs
    st.session_state.msgs = StreamlitChatMessageHistory(key="langchain_messages")
    st.session_state.msgs.clear()
    st.session_state.session_id = uuid.uuid4()
    # st.write(st.session_state.session_id)


def run_prompt(user_prompt_placeholder, bot_reply_placeholder):
    user_prompt_placeholder.chat_message("human", avatar="🗣️").write(st.session_state.prompt)

    ret = st.session_state.construct.run_prompt(bot_reply_placeholder)

    with bot_reply_placeholder:
        st.chat_message("ai", avatar="🤖").write(ret.content)




def save_hyperparameters(name):
    st.toast("Not implemented yet", icon="🚧")




























def main():
    dotenv.load_dotenv()
    st.set_page_config(page_title="LangChain intergration testing", page_icon="📖", layout="wide")

    ### INIT
    # NOTE: we no longer need this as a construct will be generated on first run, and new_chat is called then
    # if "langchain_messages" not in st.session_state:
    #     new_chat()



    ### INTERFACE
    # NOTE: if desktop mode...


    ### SIDEBAR
    with st.sidebar:
        st.title(":green[LangChain] :blue[integrator] :red[100]")
        # st.header("🦜⛓️🧠", divider="rainbow")
        # st.header(":blue[Constructs]", divider="rainbow")
        cmp_constructs()
        # st.header(":red[Debug]", divider="rainbow")



    top_of_page = st.empty()
    maincols2 = st.columns((1, 1))

    

    ### RIGHT
    # st.header("", divider="rainbow")
    with maincols2[1]:
            st.header(":orange[𝚯] :grey[Graph hyperparameters]", divider="rainbow")
            # with st.container(height=1000, border=True):
            with st.container():

                ### PRESETS
                with st.container(border=True):
                    st.selectbox("Saved presets", ["⭐️ - my fren 🐸", "Custom"], key="saved_hyperparameters")


                    cols2 = st.columns((1, 1, 1))
                    with cols2[0]:
                        with st.popover(":green[Save preset]", use_container_width=True):
                            with st.form(key="preset_form"):
                                st.text_input("preset name", key="preset_name")
                                if st.form_submit_button("Save"):
                                    save_hyperparameters(st.session_state.preset_name)

                    with cols2[1]:
                        st.button(":green[Make default]", use_container_width=True)
                    with cols2[2]:
                        st.button(":red[Clear session]", on_click=new_chat, use_container_width=True)

                # NOTE: adjusters go BEFORE affected widgets

                ### SETTINGS
                with st.container(border=True):
                    st.session_state["construct"].show_settings()

                ### AGENT PROMPTS
                with st.container():
                    st.header(":orange[📝] :grey[Agent Prompts]", divider="rainbow")
                    with st.container(border=True):
                        st.session_state["construct"].show_prompts()

                with st.container():
                    st.header("🧰 :red[Tool access]", dividgooer="rainbow")
                    # center_text("h3", "🔧 Tool access", 20)
                    with st.container(border=True):
                        st.button("🧰 :red[Open tool]", use_container_width=True)
                        st.button("📁 :orange[does nothing]", use_container_width=True)

                with st.container():
                    st.header("📁 :green[File access]", divider="rainbow")
                    with st.container(border=True):
                        st.button("📁 :green[Open file]", use_container_width=True)


    ### LEFT
    with maincols2[0]:
        # convo_history_placeholder = st.empty()
        st.header("🗣️ :blue[Conversation history]", divider="rainbow")
        # clear_button_placeholder = st.empty()
        # with st.container(height=COL_HEIGHT, border=False):
        # if len(st.session_state.langchain_messages) > 0:
        #     with st.popover("Graph state"): # Message json
        #         st.json(st.session_state.langchain_messages)
        # with st.container(height=550, border=True):
        with st.container(height=550, border=False):
        # with st.container(border=False):
            for msg in st.session_state.langchain_messages:
                st.chat_message(msg.type, avatar="🗣️" if type(msg) is HumanMessage else "🤖").write(msg.content)
            user_prompt_placeholder = st.empty()
            bot_reply_placeholder = st.empty()

            # if len(st.session_state.langchain_messages) > 0:
                # st.button(":red[Clear messages]", on_click=lambda: st.session_state.langchain_messages.clear())
                # st.header("", divider="rainbow")

        # st.markdown("---\n 📊 :blue[Conversation metrics]")
        st.header("📊 :blue[Conversation metrics]", divider="rainbow")
        with st.container(border=True):
            if len(st.session_state.langchain_messages) > 0:
                with st.popover("Graph state"): # Message json
                    st.json(st.session_state.langchain_messages)

            st.write("Session ID:", st.session_state.session_id)
            tokens = sum([len(msg.content) for msg in st.session_state.langchain_messages])
            st.write("Tokens: ", tokens)

    # with st.sidebar:
        # st.header(":green[Query]❓", divider="rainbow")
        # st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))

    # with st.sidebar:
    # colz2 = st.columns((4, 1))
    # with colz2[0]:
    #     st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))
    # with colz2[1]:
    #     clear_button_placeholder = st.empty()






    ### BOTTOM
    # run_prompt(bot_reply_placeholder)
    st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))



    # POST-PROCESSING SIDEBAR
    with st.sidebar:
        # st.header("", divider="rainbow")
        st.markdown("#")

        clear_button_placeholder = st.empty()
        draw_clear_button(clear_button_placeholder)
        st.header("", divider="rainbow")
        st.markdown("# :blue[Saved Conversations]")
        st.button("[None saved yet]", use_container_width=True, disabled=True)

        ### DEBUG
        st.header("", divider="rainbow")
        st.markdown("#")
        draw_messages()
        if len(st.session_state.langchain_messages) > 0:
            with st.popover("Graph state"): # Message json
                st.json(st.session_state.langchain_messages)

    # if len(st.session_state.langchain_messages) == 0:
    top_of_page.header("") # NOTE: This is a trick to ensure the page is scrolled to the top
    # convo_history_placeholder.header("🗣️ :blue[Conversation history]", divider="rainbow")
    V_SPACE(2)