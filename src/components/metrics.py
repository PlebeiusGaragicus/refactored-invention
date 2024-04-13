import streamlit as st

def cmp_metrics():
    st.header("📊 :blue[Metrics]", divider="rainbow")

    if len(st.session_state.langchain_messages) > 0:
        with st.popover("Graph state"): # Message json
            st.json(st.session_state.langchain_messages)

    st.text_input(":green[Session ID]", value=st.session_state.session_id, disabled=True)
    tokens = sum([len(msg.content) for msg in st.session_state.langchain_messages])
    st.text_input(":green[Tokens]", value=tokens, disabled=True)