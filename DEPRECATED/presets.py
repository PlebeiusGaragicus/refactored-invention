# import streamlit as st

# from src.database import get_db


# # TODO : cache_data this
# # def find_preset(key, default = None, is_index: bool = False, options_list: list = None):
# #     db = get_db()

# #     current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.saved_hyperparameters})

# #     # print("BUG")
# #     # print(current_preset)
# #     preset = list(current_preset)

# #     if preset == []:
# #         st.toast("No saved hyperparameters found")
# #         return default

# #     preset = preset[0]
# #     # print(preset)

# #     true_key = f"preset_{key}"
# #     # if true_key in st.session_state:
# #     if true_key in preset:
# #         if is_index:
# #             if options_list:
# #                 return options_list.index(preset[true_key])
# #             else:
# #                 raise ValueError("options_list must be provided if is_index is True")

# #         return preset[true_key]

# #     st.toast(f"Could not find preset for key: {key} - using default {default}")
# #     return default



# def save_hyperparameters(name):
#     db = get_db()

#     # current_preset = db.presets.find({"construct": st.session_state.selected_construct, "name": st.session_state.saved_hyperparameters})

#     # if list(current_preset) == []:
#     #     st.toast("You have to save the current hyperparameters first")
#     #     return

#     # ensure that the name is unique
#     # if db.presets.find_one({"name": name, "construct": st.session_state.selected_construct}):
#     #     delete_preset()
#     #     st.toast("Deleted existing preset with the same name")
#         # print("REPLACING PRESET")


#     to_save = {
#             "name": name,
#             "default": False,
#             "construct": st.session_state.selected_construct,
#         }
    
#     for s in st.session_state:
#         if s.startswith("preset_"):
#             to_save[s] = st.session_state[s]

#     if db.presets.find_one({"name": name, "construct": st.session_state.selected_construct}):
#         db.presets.update_one({"name": name, "construct": st.session_state.selected_construct}, {"$set": to_save})
#     else:
#         db.presets.insert_one(to_save)

#     # st.rerun()


# def load_presets():
#     db = get_db()

#     presets = db.presets.find({"construct": st.session_state.selected_construct})
#     presets = list(presets)

#     return presets


# def make_default():
#     db = get_db()
#     db.presets.update_many(
#         {"construct": st.session_state.selected_construct},
#         {"$set": {"default": False}}
#     )

#     db.presets.update_one(
#         {"name": st.session_state.saved_hyperparameters, "construct": st.session_state.selected_construct},
#         {"$set": {"default": True}}
#     )

#     st.rerun()



# def delete_preset():
#     db = get_db()
#     db.presets.delete_one({"name": st.session_state.saved_hyperparameters, "construct": st.session_state.selected_construct})
#     # st.rerun()


