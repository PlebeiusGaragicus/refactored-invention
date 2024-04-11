import os

import streamlit as st

from src.common import ASSETS_PATH
from src.interface import center_text

def cmp_header():
    st.set_page_config(
        # page_title="DEBUG!" if os.getenv("DEBUG", False) else "NOS4A2",
        page_title="PlebChat!",
        page_icon=os.path.join(ASSETS_PATH, "favicon.ico"),
        layout="wide",
        initial_sidebar_state="auto",
    )

    center_text("p", "🗣️🤖💬", size=60) # or h1, whichever

