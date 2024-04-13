import streamlit as st

def cmp_hyperparameters():
    st.header(":orange[𝚯] :grey[Hyperparameters]", divider="rainbow")
    # st.header(":orange[𝚯] Graph hyperparameters", divider="rainbow")
    # with st.container(height=1000, border=True):


    with st.container(border=True):
        st.session_state["construct"].show_settings()

    ### AGENT PROMPTS
    with st.container():
        st.header(":orange[📝] :blue[Prompts]", divider="rainbow")
        with st.container(border=True):
            st.session_state["construct"].show_prompts()