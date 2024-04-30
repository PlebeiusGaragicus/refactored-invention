import streamlit as st

from src.interface import build_interface

from src.database import get_db




def save_hyperparameters(name):
    db = get_db()

    # current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.selected_preset})

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

    for s in st.session_state.graph_hyperparameters.keys():
    # for s in st.session_state.graph_hyperparameters.keys():
        # if s.startswith("preset_"):
        to_save[s] = st.session_state.graph_hyperparameters[s]

    if db.presets.find_one({"name": name, "construct": st.session_state.selected_construct}):
        db.presets.update_one({"name": name, "construct": st.session_state.selected_construct}, {"$set": to_save})
    else:
        db.presets.insert_one(to_save)



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
        {"name": st.session_state.selected_preset, "construct": st.session_state.selected_construct},
        {"$set": {"default": True}}
    )

    st.rerun()



def delete_preset():
    db = get_db()
    db.presets.delete_one({"name": st.session_state.selected_preset, "construct": st.session_state.selected_construct})
    # st.rerun()



















def cmp_hyperparameters():
    st.header("🎛️ :orange[Hyperparameters]", divider="rainbow", anchor="Hyperparameters")

    cols3 = st.columns((1, 2, 1))
    with cols3[0]:
        with st.popover("✍️ :blue[Edit]", use_container_width=True):
            if st.button(":orange[⭐️ Make default]", use_container_width=True):
                make_default()
            if st.button(":blue[💾 Save!!]", use_container_width=True):
                save_hyperparameters(st.session_state.selected_preset)
                # st.rerun()
            with st.form(key="preset_form", clear_on_submit=True):
                st.markdown(":green[Save as new preset]")
                st.text_input("Preset name", key="new_preset_name", label_visibility='collapsed')
                if st.form_submit_button("🌱 :green[Save as new]", use_container_width=False):
                    save_hyperparameters(st.session_state.new_preset_name)
                    st.rerun()




    with cols3[1]:
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
            # options[index_of_default] = f"⭐ {default_preset}" # this makes it so the preset isn't found and isn't loaded... a shame, really
        st.selectbox(label="selected_preset", options=options, key="selected_preset", label_visibility="collapsed", index=index_of_default)




    with cols3[2]:
        with st.popover("🗑️ :red[Delete]", use_container_width=True):
            st.warning("Are you sure?!")
            if st.button(":red[Delete]", use_container_width=True):
                delete_preset()
                st.rerun()





    with st.container(height=400, border=True):
        build_interface( st.session_state["construct"].interface_config() )





















































# def cmp_presets():
#     st.header(":violet[Saved Configurations]", divider="rainbow", anchor="presets")
#     with st.container(border=True):

#         presets = load_presets()
#         if presets:
#             options = [preset["name"] for preset in presets]
#         else:
#             options = []

#         index_of_default = 0
#         default_preset = [preset["name"] for preset in presets if preset["default"]]
#         if default_preset:
#             default_preset = default_preset[0]
#             index_of_default = options.index(default_preset)
#             # options[index_of_default] = f"⭐ {default_preset}" # this makes it so the preset isn't found and isn't loaded... a shame, really
#         st.selectbox(label="selected_preset", options=options, key="selected_preset", label_visibility="collapsed", index=index_of_default)

#         # db = get_db()
#         # current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.selected_preset})
#         # st.session_state.current_preset = list(current_preset)

#         cl2 = st.columns((2, 1))
#         with cl2[0]:
#             with st.popover(":green[Save as new preset]", use_container_width=True):
#                 with st.form(key="preset_form", clear_on_submit=True):
#                     st.text_input("preset name", key="new_preset_name")
#                     if st.form_submit_button("Save"):
#                         save_hyperparameters(st.session_state.new_preset_name)
#                         st.rerun()

#         with cl2[1]:
#             # if st.button(":blue[💾 Save]", use_container_width=True, disabled=st.session_state.current_preset == []):
#             if st.button(":blue[💾 Save]", use_container_width=True, disabled=st.session_state.selected_preset is None):
#                 # delete_preset()
#                 save_hyperparameters(st.session_state.selected_preset)
#                 st.rerun()


#         cols2 = st.columns((1.3, 1))
#         with cols2[0]:
#             if st.button(":green[⭐️ Make default]", use_container_width=True):
#                 make_default()

#         with cols2[1]:
#             with st.popover("🗑️ :red[Delete]", use_container_width=True):
#                 st.warning("Are you sure!?")
#                 if st.button(":red[Delete]", use_container_width=True):
#                     delete_preset()
#                     st.rerun()

