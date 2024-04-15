import pymongo

import streamlit as st

@st.cache_resource
def get_db():
    return pymongo.MongoClient("mongodb://localhost:27017/")["plebchat"]




def main():
    st.title("db_viewer")

    db = get_db()

    st.write("Collections:")
    st.write(db.list_collection_names())

    # for each preset, show a button to delete it
    st.write("Presets:")
    presets = db.presets.find()
    for preset in presets:
        with st.container(border=True):
            # st.write("# Preset:", preset["name"])
            st.write(f"## :blue[{preset['name']}]")
            st.write("**Construct:**", preset["construct"])
            st.write("Default:", preset["default"])
            with st.container(border=True):
                for key, value in preset.items():
                    # if key.startswith("*"):
                    st.write(f"{key}: `{value}`")

            if st.button(f"Delete", key=preset["_id"]):
                db.presets.delete_one({"_id": preset["_id"]})
                st.rerun()
