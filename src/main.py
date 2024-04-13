import dotenv

import streamlit as st

from src.interface import center_text
# from TESTING.common import cprint, Colors, FILES_DIR
from src.components.vector_database import cmp_vector_database
from src.components.metrics import cmp_metrics
from src.components.hyperparameters import cmp_hyperparameters
from src.components.presets import cmp_presets
from src.components.tools import cmp_tools
from src.components.sidebar import cmp_constructs, cmp_saved_conversations, cmp_debug
from src.components.convo_history import cmp_convo_history



# https://github.com/langchain-ai/streamlit-agent
def main():

    dotenv.load_dotenv()
    st.set_page_config(page_title="LangChain intergration testing", page_icon="📖", layout="wide")

    ### INIT
    # NOTE: we no longer need this as a construct will be generated on first run, and new_chat is called then
    # if "langchain_messages" not in st.session_state:
    #     new_chat()


    # NOTE: if desktop mode...
    ### SIDEBAR
    with st.sidebar:
        center_text("h1", "🗣️🦜💬", 40)
        # st.title(":green[LangChain] :blue[integrator] :red[100]")
        with st.container(border=True):
            cmp_constructs()
        st.header("", divider="rainbow")


    cmp_presets()

    maincols2 = st.columns((1, 1))
    
    ### RIGHT
    with maincols2[0]:
        cmp_hyperparameters()

    ### LEFT
    with maincols2[1]:
        cmp_tools()

        # with st.container():
        cmp_vector_database()


    st.header("", divider=True)


    ### BOTTOM
    bcol2 = st.columns((2, 1))
    with bcol2[1]:
        cmp_metrics()


    with bcol2[0]:
        cmp_convo_history()


    # POST-PROCESSING SIDEBAR
    with st.sidebar:
        cmp_saved_conversations()

        ### DEBUG
        cmp_debug()
