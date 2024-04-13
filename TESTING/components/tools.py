import streamlit as st

def cmp_tools():
    st.header("🧰 :red[Tool binding]", divider="rainbow")

    with st.container(border=True):
        for tool in ["📁 file store", "🕸️ web search", "🧮 code execution", "🔍 query analysis", "📝 revision"]:
            clz = st.columns((3, 1))
            with clz[0]:
                with st.popover(f":red[{tool}]", use_container_width=True):
                    st.error("Not yet implemented")
            with clz[1]:
                st.checkbox("`enable`", key=f"enable_{tool}")
