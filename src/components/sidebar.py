import uuid

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st

from src.constructs import all_constructs
from src.interface import center_text

from src.database import get_db





def cmp_constructs():
    construct_names = [c.name for c in all_constructs()]
    db = get_db()



    def load_construct():
        # construct_names = [c.name for c in ALL_CONSTRUCTS]
        # st.session_state.selected_construct = selected
        # selected = st.session_state.selected_construct

        for Construct in all_constructs():
            if Construct.name == st.session_state.selected_construct:
                st.session_state["construct"] = Construct()

        db.user_settings.update_one({"key": "selected_construct"}, {"$set": {"value": st.session_state.selected_construct}}, upsert=True)
        st.toast(f"Switched to {st.session_state.selected_construct}!", icon=st.session_state["construct"].avatar)
        new_chat()


    # Initialize or load the selection from the database if not in the session state
    # if "selected_construct" not in st.session_state:
    if "construct" not in st.session_state:
        st.toast("Welcome to PlebChat!", icon="🎉")
        selected_construct = db.user_settings.find_one({"key": "selected_construct"})
        if selected_construct and selected_construct["value"] in construct_names:
            selected_construct = selected_construct["value"]
        else:
            selected_construct = construct_names[0]
            st.warning("No construct selection saved in database.")
    else:
        selected_construct = st.session_state.selected_construct

        # load_construct()




    # selected = st.radio(
    st.radio(
        "choose a construct",
        options=construct_names,
        horizontal=True,
        index=construct_names.index(selected_construct),
        label_visibility="collapsed",
        key="selected_construct",
        on_change=load_construct)


    if 'construct' not in st.session_state:
        load_construct()






def new_chat():
    # Note: new messages are saved to history automatically by Langchain during run
    # https://api.python.langchain.com/en/latest/chat_message_histories/langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory.html
    # if "msgs" in st.session_state:
        # del st.session_state.msgs
    st.session_state.msgs = StreamlitChatMessageHistory(key="convo_history")
    st.session_state.msgs.clear()
    st.session_state.session_id = uuid.uuid4()
    # st.write(st.session_state.session_id)




def draw_clear_button(container):
    with container:
        # if len(st.session_state.convo_history) > 0:
            # st.button("🗑️ :red[Clear messages]", on_click=lambda: st.session_state.convo_history.clear(), use_container_width=True)

        clz2 = st.columns((1, 1))
        with clz2[0]:
            # st.button("🌱 :green[New]", on_click=lambda: st.session_state.convo_history.clear(), use_container_width=True, disabled=not len(st.session_state.convo_history))
            st.button("🗑️ :red[Clear]", on_click=lambda: st.session_state.convo_history.clear(), use_container_width=True, disabled=not len(st.session_state.convo_history))
        with clz2[1]:
            st.button("💾 :blue[Save]", on_click=lambda: st.session_state.convo_history.clear(), use_container_width=True, disabled=not len(st.session_state.convo_history))


def cmp_links():
    st.header("", divider="rainbow")
    # st.markdown("# :blue[Links]")
    # st.write(":orange[𝚯] [Hyperparameters](#Hyperparameters)")
    # st.write("🔧 [Tools](#Tools)")
    # st.write("🗄️ [Vector Database](#VectorDatabase)")
    # st.write("🗣️💬 [Conversation history](#ConvoHistory)")
    st.markdown("""# :blue[Links]
:orange[𝚯] [Hyperparameters](#Hyperparameters)

🗄️ [Vector Database](#VectorDatabase)

🔧 [Tools](#Tools)

🗣️💬 [Conversation history](#ConvoHistory)

""")
    # st.write("")
    # st.write("🗣️💬 [Conversation history](#ConvoHistory)")
    


def cmp_saved_conversations():
    # st.header(":blue[Saved Conversations]", divider="rainbow")
    # st.markdown(".")
    # if len(st.session_state.convo_history) > 0:
    #     clear_button_placeholder = st.empty()
    #     draw_clear_button(clear_button_placeholder)
    #     center_text("p", "---", 7)

    # pass
    # with st.popover(":blue[Saved Conversations]", use_container_width=True):
    with st.expander(":blue[Saved Conversations]"):
        for _ in range(10):
            st.button(f"Button {_} button yay ayyy y yaya!!", use_container_width=True)

        st.write("---")
        st.button("➕ Load more", use_container_width=True)


def draw_messages():
    with st.expander("Debug", expanded=False):
        st.write(st.session_state)
        st.write(st.session_state.construct)

    # st.markdown(st.session_state.msgs) # class 'langchain_community.chat_message_histories.streamlit.StreamlitChatMessageHistory
    # st.markdown(type(st.session_state.convo_history)) # list




def cmp_debug():
    st.header("🪲 :red[Debug]", divider="rainbow")
    draw_messages()
    if len(st.session_state.convo_history) > 0:
        with st.popover("Graph state"): # Message json
            st.json(st.session_state.convo_history)
