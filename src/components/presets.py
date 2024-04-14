import streamlit as st

from src.database import get_db


# TODO : cache_data this
def find_preset(key, default = None, is_index: bool = False, options_list: list = None):
    db = get_db()

    current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.saved_hyperparameters})

    print("BUG")
    # print(current_preset)
    preset = list(current_preset)

    if preset == []:
        st.toast("No saved hyperparameters found")
        return default

    preset = preset[0]
    print(preset)

    true_key = f"*{key}"
    # if true_key in st.session_state:
    if true_key in preset:
        if is_index:
            if options_list:
                return options_list.index(preset[true_key])
            else:
                raise ValueError("options_list must be provided if is_index is True")

        return preset[true_key]

    st.toast(f"Could not find preset for key: {key} - using default {default}")
    return default



def save_hyperparameters(name):
    db = get_db()

    # current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.saved_hyperparameters})

    # if list(current_preset) == []:
    #     st.toast("You have to save the current hyperparameters first")
    #     return

    # ensure that the name is unique
    # if db.presets.find_one({"name": name, "construct": st.session_state.selected_construct}):
    #     delete_preset()
    #     st.toast("Deleted existing preset with the same name")
        # print("REPLACING PRESET")


    to_save = {
            "name": name,
            "default": False,
            "construct": st.session_state.selected_construct,
        }
    
    for s in st.session_state:
        if s.startswith("*"):
            to_save[s] = st.session_state[s]

    if db.presets.find_one({"name": name, "construct": st.session_state.selected_construct}):
        db.presets.update_one({"name": name, "construct": st.session_state.selected_construct}, {"$set": to_save})
        print("REPLACING PRESET")
    else:
        db.presets.insert_one(to_save)

    # st.rerun()


def load_presets():
    db = get_db()

    presets = db.presets.find({"construct": st.session_state.selected_construct})
    presets = list(presets)

    return presets


def make_default():
    db = get_db()
    db.presets.update_many(
        {"construct": st.session_state.selected_construct},
        {"$set": {"default": False}}
    )

    db.presets.update_one(
        {"name": st.session_state.saved_hyperparameters, "construct": st.session_state.selected_construct},
        {"$set": {"default": True}}
    )

    st.rerun()



def delete_preset():
    db = get_db()
    db.presets.delete_one({"name": st.session_state.saved_hyperparameters, "construct": st.session_state.selected_construct})
    # st.rerun()




def cmp_presets():
    st.sidebar.markdown("# :violet[Saved Graph Configurations]")
    with st.sidebar.container(border=True):

        presets = load_presets()
        if presets:
            options = [preset["name"] for preset in presets]
        else:
            options = []

        index_of_default = 0
        default_preset = [preset["name"] for preset in presets if preset["default"]]
        if default_preset:
            default_preset = default_preset[0]
            index_of_default = options.index(default_preset)
            # options[index_of_default] = f"⭐ {default_preset}"
        st.selectbox(label="saved_hyperparameters", options=options, key="saved_hyperparameters", label_visibility="collapsed", index=index_of_default)

        # db = get_db()
        # current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.saved_hyperparameters})
        # st.session_state.current_preset = list(current_preset)

        cl2 = st.columns((2, 1))
        with cl2[0]:
            with st.popover(":green[Save as new preset]", use_container_width=True):
                with st.form(key="preset_form", clear_on_submit=True):
                    st.text_input("preset name", key="preset_name")
                    if st.form_submit_button("Save"):
                        save_hyperparameters(st.session_state.preset_name)
                        st.rerun()

        with cl2[1]:
            # if st.button(":blue[💾 Save]", use_container_width=True, disabled=st.session_state.current_preset == []):
            if st.button(":blue[💾 Save]", use_container_width=True, disabled=False):
                # delete_preset()
                save_hyperparameters(st.session_state.saved_hyperparameters)
                st.rerun()


        cols2 = st.columns((1.3, 1))
        with cols2[0]:
            if st.button(":green[⭐️ Make default]", use_container_width=True):
                make_default()

        with cols2[1]:
            with st.popover("🗑️ :red[Delete]", use_container_width=True):
                st.warning("Are you sure!?")
                if st.button(":red[Delete]", use_container_width=True):
                    delete_preset()
                    st.rerun()

