import pymongo

import streamlit as st

@st.cache_resource
def get_db():
    return pymongo.MongoClient("mongodb://localhost:27017/")["plebchat"]
