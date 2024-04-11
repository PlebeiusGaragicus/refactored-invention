import streamlit as st

from src.components.header import cmp_header


def main_page():

    cmp_header()


    if prompt := st.chat_input("Ask a question.", key="user_input"):
        with st.chat_message(name="user"):
            st.write(prompt)
