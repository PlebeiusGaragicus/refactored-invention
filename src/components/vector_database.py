import dotenv
import os
import pathlib

import streamlit as st

from src.common import FILES_DIR



def cmp_vector_database():
    st.header("🗄️ :green[Vector database]", divider="rainbow", anchor="VectorDatabase")

    cols2 = st.columns((1, 2, 1))
    with cols2[0]:
        with st.popover("🆕 :green[New]", use_container_width=True):
            st.error("Not yet implemented")

    with cols2[1]:
        st.selectbox("Select vectorstore", ["🧠 Research", "💬 past_convos", "🐸 Memes"], key="selected_vector", label_visibility="collapsed")

    with cols2[2]:
        with st.popover("📄 :blue[Upload]", use_container_width=True):
            with st.form(key="add_file", clear_on_submit=True):
                # st.text_input("Description", key="file_desc")

                st.file_uploader("Upload file", key="file_upload", accept_multiple_files=True)
                # NOTE: if you allow multiple files then it returns a list... #TODO
                # st.file_uploader("Upload file", key="file_upload")

                if st.form_submit_button(":blue[Upload]"):
                    # if st.session_state.file_upload and st.session_state.file_desc:
                    if st.session_state.file_upload:
                        for file in st.session_state.file_upload:

                            # check if file exists
                            # if (FILES_DIR / st.session_state.file_upload.name).exists():
                            if (FILES_DIR / file.name).exists():
                                st.toast("File already exists", icon="🚫")

                            else:
                                # if file is not None:
                                with open(FILES_DIR / file.name, 'wb') as f:
                                    f.write(file.getvalue())
                                st.toast("Upload successful", icon="✅")
                    else:
                        st.toast("Select a file to upload", icon="🚫")


    with st.container(height=300, border=True):

        files = [f for f in FILES_DIR.iterdir() if f.is_file()]
        for file in files:
            icon = "💾"
            if file.suffix.lower() in [".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"]:
                icon = "📑"
            elif file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff", ".tif", ".heic", ".heif"]:
                icon = "🖼️"

            if len(file.name) > 55:
                file_name = file.name[:55] + "..."
            else:
                file_name = file.name
            with st.expander(f"{icon} :grey[{file_name}]", expanded=False):
                file_size_kb = file.stat().st_size / 1024
                if file_size_kb > 1024:
                    st.write(f"File size: `{file_size_kb / 1024:.1f}` MB")
                else:
                    st.write(f"File size: `{file_size_kb:.1f}` KB")
                
                if st.button("🗑️ :red[Delete]", key=f"delete_{file}"):
                    file.unlink()
                    st.toast("File deleted", icon="🗑️")
                    st.rerun()
