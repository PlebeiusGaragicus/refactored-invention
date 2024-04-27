import streamlit as st


# TODO - review the CRAG code: https://github.com/PlebeiusGaragicus/CRAG

# INSPIRATION:
# https://github.com/mistralai/cookbook/blob/main/third_party/langchain/corrective_rag_mistral.ipynb
# https://github.com/mistralai/cookbook/tree/main/third_party/langchain
# https://www.youtube.com/watch?v=eOo4GfHj3ZE
# https://www.youtube.com/watch?v=sgnrL7yo1TE
# https://blog.langchain.dev/query-construction/


class Colors():
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

def color(color: Colors):
    return f'\033[1;3{color}m'

def reset_color():
    return '\033[0m'

def cprint(string: str, color: Colors, end='\n'):
    print_this = f'\033[1;3{color}m' + string + '\033[0m'
    print(print_this, end=end)

def cput(string: str, color: Colors):
    print_this = f'\033[1;3{color}m' + string + '\033[0m'
    print(print_this, end='', flush=True)


def change_color(color: Colors):
    print(f'\033[1;3{color}m')





def create_slider(name, min_value, max_value, default=None, step=None):
    return {
        "name": name,
        "type": "float",
        "widget": "slider",
        "min": min_value,
        "max": max_value,
        "default": default if default is not None else min_value,
        "step": step
    }

def create_selectbox(name, options, default=None):
    return {
        "name": name,
        "type": "string",
        "widget": "selectbox",
        "options": options,
        "default": default if default else options[0]
    }

def create_checkbox(name, default=False):
    return {
        "name": name,
        "type": "bool",
        "widget": "checkbox",
        "default": default
    }

def create_text_area(name, default=''):
    return {
        "name": name,
        "type": "string",
        "widget": "text_area",
        "default": default
    }



def build_interface(config):
    if "graph_hyperparameters" not in st.session_state:
        st.session_state.graph_hyperparameters = {}

    st.header(":orange[Θ] Hyperparameters", divider="rainbow")
    with st.container(border=True):

        for widget in config["widgets"]:
            if widget["widget"] == "slider":
                st.session_state.graph_hyperparameters[widget["name"]] = st.slider(
                    label=widget["name"],
                    min_value=widget["min"],
                    max_value=widget["max"],
                    value=widget["default"]
                )
            elif widget["widget"] == "selectbox":
                st.session_state.graph_hyperparameters[widget["name"]] = st.selectbox(
                    label=widget["name"],
                    options=widget["options"]
                )
            elif widget["widget"] == "checkbox":
                st.session_state.graph_hyperparameters[widget["name"]] = st.checkbox(
                    label=widget["name"],
                    value=widget["default"]
                )
            elif widget["widget"] == "text_area":
                st.session_state.graph_hyperparameters[widget["name"]] = st.text_area(
                    label=widget["name"],
                    value=widget["default"]
                )
