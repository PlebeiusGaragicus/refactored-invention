import streamlit as st

COL_HEIGHT = 550


def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')


def center_text(type, text, size=None):
    if size == None:
        st.write(f"<{type} style='text-align: center;'>{text}</{type}>", unsafe_allow_html=True)
    else:
        st.write(f"<{type} style='text-align: center; font-size: {size}px;'>{text}</{type}>", unsafe_allow_html=True)




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







# def create_slider(name, min_value, max_value, default=None, step=None, help=None):
def numeric_parameter(name, min_value, max_value, default=None, step=None, help=None):
    return {
        "name": name,
        "type": "float",
        "widget": "slider",
        "min": min_value,
        "max": max_value,
        "default": default if default is not None else min_value,
        "step": step,
        "help": help
    }

# def create_selectbox(name, options, default=None, help=None):
def options_parameter(name, options, default=None, help=None):
    return {
        "name": name,
        "type": "string",
        "widget": "selectbox",
        "options": options,
        "default": default if default else options[0],
        "help": help
    }

# def create_checkbox(name, default=False, help=None):
def boolean_parameter(name, default=False, help=None):
    return {
        "name": name,
        "type": "bool",
        "widget": "checkbox",
        "default": default,
        "help": help
    }

# def create_text_area(name, default='', help=None):
def text_parameter(name, default='', help=None):
    return {
        "name": name,
        "type": "string",
        "widget": "text_input",
        "default": default,
        "help": help
    }

def prompt_parameter(name, default='', help=None):
    return {
        "name": name,
        "type": "text_area",
        "widget": "text_area",
        "default": default,
        "help": help
    }


def build_interface(config):
    if "graph_hyperparameters" not in st.session_state:
        st.session_state.graph_hyperparameters = {}

        # load the user's saved hyperparameter
        if "selected_preset" in st.session_state:
            from src.components.hyperparameters import load_presets
            selected_preset = st.session_state.selected_preset
            presets = load_presets()
            st.session_state.loaded_preset = [preset for preset in presets if preset["name"] == selected_preset]
            st.session_state.loaded_preset = st.session_state.loaded_preset[0] if st.session_state.loaded_preset else {}



    for widget in config["widgets"]:
        if widget["widget"] == "slider":
            st.session_state.graph_hyperparameters[widget["name"]] = st.slider(
                # label=widget["name"],
                label=f"**:blue[{widget["name"].replace('_', ' ')}]**",
                # label=f":red[{widget["name"]}]",
                key=widget["name"],
                min_value=widget["min"],
                max_value=widget["max"],
                # value=widget["default"],
                value=st.session_state.loaded_preset.get(widget["name"], widget["default"]),
                help=widget.get("help", None),  
            )
        elif widget["widget"] == "selectbox":
                try:
                    index = widget["options"].index(st.session_state.loaded_preset.get(widget["name"], widget["default"]))
                except ValueError:
                    index=0

                with st.container(border=True):
                # st.session_state.graph_hyperparameters[widget["name"]] = st.selectbox(
                    st.session_state.graph_hyperparameters[widget["name"]] = st.radio(
                    # label=widget["name"],
                    label=f"**:blue[{widget["name"].replace('_', ' ')}]**",
                    # label=f":blue[{widget["name"]}]",
                    key=widget["name"],
                    options=widget["options"],
                    # index=widget["options"].index(widget["default"]),
                    index=index,
                    help=widget.get("help", None),
                )
        elif widget["widget"] == "checkbox":
            st.session_state.graph_hyperparameters[widget["name"]] = st.checkbox(
                # label=widget["name"],
                label=f"**:blue[{widget["name"].replace('_', ' ')}]**",
                # label=f":orange[{widget["name"]}]",
                key=widget["name"],
                # value=widget["default"],
                value=st.session_state.loaded_preset.get(widget["name"], widget["default"]),
                help=widget.get("help", None),
            )
        elif widget["widget"] == "text_input":
            st.session_state.graph_hyperparameters[widget["name"]] = st.text_input(
                label=f"**:blue[{widget["name"].replace('_', ' ')}]**",
                # label=f":green[{widget["name"]}]",
                key=widget["name"],
                value=st.session_state.loaded_preset.get(widget["name"], widget["default"]),
                # value=widget["default"],
                help=widget.get("help", None),
            )
        elif widget["widget"] == "text_area":
            st.session_state.graph_hyperparameters[widget["name"]] = st.text_area(
                label=f"**:blue[{widget["name"].replace('_', ' ')}]**",
                # label=f":green[{widget["name"]}]",
                key=widget["name"],
                value=st.session_state.loaded_preset.get(widget["name"], widget["default"]),
                # value=widget["default"],
                help=widget.get("help", None),
                height=180
            )
        else:
            st.error(f"Unknown widget type: {widget['widget']}")
            st.stop()
