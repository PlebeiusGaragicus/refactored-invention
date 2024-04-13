import dotenv
import os
import pathlib
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


FILES_DIR = pathlib.Path(__file__).parent.parent / "FILES"

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

        clz2 = st.columns((1, 1))
        with clz2[0]:
            # st.button("🌱 :green[New]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))
            st.button("🗑️ :red[Clear]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))
        with clz2[1]:
            st.button("💾 :blue[Save]", on_click=lambda: st.session_state.langchain_messages.clear(), use_container_width=True, disabled=not len(st.session_state.langchain_messages))


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
        center_text("h1", "🗣️🦜💬", 40)
        # st.title(":green[LangChain] :blue[integrator] :red[100]")
        # st.header(":blue[Constructs]", divider="rainbow")
        with st.container(border=True):
            cmp_constructs()
        st.header("", divider="rainbow")
        # st.header(":red[Debug]", divider="rainbow")



    top_of_page = st.empty()
    maincols2 = st.columns((1, 1))

    
    st.sidebar.markdown("# :violet[Saved Graph Configurations]")
    with st.sidebar.container(border=True):
        st.selectbox(label="saved_hyperparameters", options=["⭐️ - my fren 🐸", "Custom"], key="saved_hyperparameters", label_visibility="collapsed")


        with st.popover(":green[Save as new preset]", use_container_width=True):
            with st.form(key="preset_form"):
                st.text_input("preset name", key="preset_name")
                if st.form_submit_button("Save"):
                    save_hyperparameters(st.session_state.preset_name)
        cols2 = st.columns((1, 1))
        with cols2[0]:

        # with cols2[1]:
            st.button(":green[Make default]", use_container_width=True)
        with cols2[1]:
            with st.popover("🗑️ :red[Delete]", use_container_width=True):
                st.error("R U SURE?")
                st.button(":red[Delete]", use_container_width=True)
            # st.button(":red[Delete preset]", on_click=new_chat, use_container_width=True)







    ### RIGHT
    # st.header("", divider="rainbow")
    with maincols2[0]:
        st.header(":orange[𝚯] :grey[Hyperparameters]", divider="rainbow")
        # st.header(":orange[𝚯] Graph hyperparameters", divider="rainbow")
        # with st.container(height=1000, border=True):
        with st.container():

            ### PRESETS

            # NOTE: adjusters go BEFORE affected widgets

            ### SETTINGS
            with st.container(border=True):
                st.session_state["construct"].show_settings()

            ### AGENT PROMPTS
            with st.container():
                st.header(":orange[📝] :blue[Prompts]", divider="rainbow")
                with st.container(border=True):
                    st.session_state["construct"].show_prompts()


    ### LEFT
    with maincols2[1]:
        with st.container():
            # st.header(":red[🔧 Tools]", divider="rainbow")
            st.header("🧰 :red[Tool binding]", divider="rainbow")
            # cols2 = st.columns((1, 1))
            # # with cols2[0]:
            # #     pass
            # with cols2[0]:
            #     with st.popover("Add tool", use_container_width=True):
            #         with st.form(key="tool_form"):
            #             st.text_input("tool name", key="tool_name")
            #             st.text_area("tool description", key="tool_description")
            #             if st.form_submit_button("Add tool"):
            #                 st.toast("Not yet implemented", icon="🚧")

            with st.container(border=True):
                for tool in ["📁 file store", "🕸️ web search", "🧮 code execution", "🔍 query analysis", "📝 revision"]:
                    clz = st.columns((3, 1))
                    with clz[0]:
                        with st.popover(f":red[{tool}]", use_container_width=True):
                            st.error("Not yet implemented")
                    with clz[1]:
                        st.checkbox("`enable`", key=f"enable_{tool}")
                # st.button("🧰 :red[Open tool]", use_container_width=True)
                # st.button("does nothing", use_container_width=True)
                # st.button("does something", use_container_width=True)
                # st.button("does not a thing", use_container_width=True)

        with st.container():
            st.header("🗄️ :green[Vector database]", divider="rainbow")

            cols2 = st.columns((1, 1))
            with cols2[1]:
                with st.popover("📄 :blue[Upload file]", use_container_width=True):
                    with st.form(key="add_file", clear_on_submit=True):
                        st.text_input("Description", key="file_desc")

                        # st.file_uploader("Upload file", key="file_upload", accept_multiple_files=True)
                        # NOTE: if you allow multiple files then it returns a list... #TODO
                        st.file_uploader("Upload file", key="file_upload")

                        if st.form_submit_button(":blue[Upload]"):
                            if st.session_state.file_upload and st.session_state.file_desc:

                                # check if file exists
                                if (FILES_DIR / st.session_state.file_upload.name).exists():
                                    st.toast("File already exists", icon="🚫")

                                else:
                                    if st.session_state.file_upload is not None:
                                        with open(FILES_DIR / st.session_state.file_upload.name, 'wb') as f:
                                            f.write(st.session_state.file_upload.getvalue())
                                    st.toast("Upload successful", icon="✅")
                            else:
                                st.toast("Missing file or description", icon="🚫")

            with cols2[0]:
                st.selectbox("Select vectorstore", ["📄 datastore.txt", "📄 past_convo12.txt", "📄 research1.pdf", "📄 img_23438.png"], key="selected_vector", label_visibility="collapsed")

            with st.container(height=300, border=True):
                # for file in ["📄 datastore.txt", "📄 past_convo12.txt", "📄 research1.pdf", "📄 img_23438.png"]:
                #     with st.expander(f":grey[{file}]", expanded=False):
                #         st.write("-- file content --")

                # get list of files
                files = [f for f in FILES_DIR.iterdir() if f.is_file()]
                for file in files:
                    icon = "💾"
                    if file.suffix.lower() in [".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"]:
                        icon = "📑"
                    elif file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff", ".tif", ".heic", ".heif"]:
                        icon = "🖼️"

                    with st.expander(f"{icon} :grey[{file.name}]", expanded=False):
                        file_size_kb = file.stat().st_size / 1024
                        if file_size_kb > 1024:
                            st.write(f"File size: `{file.stat().st_size / 1024:.2f}` MB")
                        else:
                            st.write(f"File size: `{file_size_kb:.2f}` KB")
                        
                        if st.button("🗑️ :red[Delete]", key=f"delete_{file}"):
                            file.unlink()
                            st.toast("File deleted", icon="🗑️")
                            st.rerun()
        


    st.header("", divider=True)



    ### BOTTOM
    bcol2 = st.columns((2, 1))

    with bcol2[1]:
        with st.container():
            st.header("📊 :blue[Metrics]", divider="rainbow")
            # with st.container(border=True):
            with st.container():
                if len(st.session_state.langchain_messages) > 0:
                    with st.popover("Graph state"): # Message json
                        st.json(st.session_state.langchain_messages)

                st.text_input(":green[Session ID]", value=st.session_state.session_id, disabled=True)
                # st.write(f"Session ID:")
                # st.write(st.session_state.session_id)
                tokens = sum([len(msg.content) for msg in st.session_state.langchain_messages])
                st.text_input(":green[Tokens]", value=tokens, disabled=True)
                # st.write("Tokens: ", tokens)



    # with st.container(height=500, border=True):
    with bcol2[0]:
        st.header("🗣️💬 :rainbow[Conversation history]", divider="rainbow")

        with st.container(height=500, border=True):
        # with st.container(border=False):

            for msg in st.session_state.langchain_messages:
                st.chat_message(msg.type, avatar="🗣️" if type(msg) is HumanMessage else "🤖").write(msg.content)
            user_prompt_placeholder = st.empty()
            bot_reply_placeholder = st.empty()




        st.chat_input("🎯 Ask me anything", key="prompt", on_submit=run_prompt, args=(user_prompt_placeholder, bot_reply_placeholder,))



    # POST-PROCESSING SIDEBAR
    with st.sidebar:
        st.header("", divider="rainbow")

        st.markdown("# :blue[Saved Conversations]")
        # st.markdown(".")
        if len(st.session_state.langchain_messages) > 0:
            clear_button_placeholder = st.empty()
            draw_clear_button(clear_button_placeholder)
            center_text("p", "---", 7)

        #TODO - implement saved conversations
        st.button("[None saved yet]", use_container_width=True, disabled=True)

        ### DEBUG
        st.header("", divider="rainbow")
        st.markdown("#")
        draw_messages()
        if len(st.session_state.langchain_messages) > 0:
            with st.popover("Graph state"): # Message json
                st.json(st.session_state.langchain_messages)

    # st.header(".")