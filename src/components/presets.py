import streamlit as st



def save_hyperparameters(name):
    st.toast("Not implemented yet", icon="🚧")





def cmp_presets():
    st.sidebar.markdown("# :violet[Saved Graph Configurations]")
    with st.sidebar.container(border=True):
        st.selectbox(label="saved_hyperparameters", options=["⭐️ - my fren 🐸", "Custom"], key="saved_hyperparameters", label_visibility="collapsed")

        with st.popover(":green[Save as new preset]", use_container_width=True):
            with st.form(key="preset_form"):
                st.text_input("preset name", key="preset_name")
                if st.form_submit_button("Save"):
                    save_hyperparameters(st.session_state.preset_name)
        cols2 = st.columns((1, 1))
        with cols2[0]:

            st.button(":green[Make default]", use_container_width=True)
        with cols2[1]:
            with st.popover("🗑️ :red[Delete]", use_container_width=True):
                st.warning("Are you sure!?")
                st.button(":red[Delete]", use_container_width=True)