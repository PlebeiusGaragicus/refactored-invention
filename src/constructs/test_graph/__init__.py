from typing import Annotated, Literal

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

import streamlit as st

from src.interface import (
    Colors,
    cprint,
    numeric_parameter,
    options_parameter,
    boolean_parameter,
    text_parameter,
    prompt_parameter
)




class State(TypedDict):
    input: str
    messages: Annotated[list, add_messages]
    something_random: int





def bad_route(state: State, config: RunnableConfig):
    cprint("\n--- NODE: bad_route() ---", Colors.MAGENTA)
    cprint("### THIS SHOULD NEVER HAPPEN!!! ###", Colors.RED)

    return {"messages": [AIMessage(content="I'm sorry, I don't understand that question.")]}



# def build_graph(use_open_routing: bool):

#     from src.constructs.test_graph.router import route_OpenAI, route_Ollama
#     from src.constructs.test_graph.friendly_chatbot import friendly_chatbot
#     from src.constructs.test_graph.vector_store import vectorstore


#     # workflow = StateGraph(GraphState)
#     graph_builder = StateGraph(State)


#     graph_builder.add_node("vectorstore", vectorstore)
#     graph_builder.add_edge("vectorstore", END)
#     graph_builder.add_node("friendly_chatbot", friendly_chatbot)
#     graph_builder.add_edge("friendly_chatbot", END)
#     graph_builder.add_node("bad_route", bad_route)
#     graph_builder.add_edge("bad_route", END)

#     graph_builder.set_conditional_entry_point(
#                     route_OpenAI if use_open_routing else route_Ollama,
#                     {
#                         "vectorstore": "vectorstore",
#                         "friendly_chatbot": "friendly_chatbot",
#                         "bad_route": "bad_route"
#                     }
#                 )


#     graph = graph_builder.compile()
#     return graph

from src.constructs import PlebGraph





class TestGraph(PlebGraph):
    """ This is the docstring to the graph class!  Whoopiee!"""
    name: str = "TestGraph"
    avatar: str = "🛠️"

    @classmethod
    def interface_config(self):
        MODEL_OPTIONS = ['gemma:2b', 'mistral:7b', 'dolphin-mistral:latest', 'OpenAI']

        return {
            # "graph_name": "Example Graph",
            "widgets": [
                # TODO rename these to - numeric_parameter, options_parameter, boolean_parameter, text_parameter
                numeric_parameter("llm_temperature", 0.0, 1.0, default=0.8, help="The temperature of the LLM"),
                options_parameter("llm_model", MODEL_OPTIONS, default="gemma:2b", help="The LLM model to use"),
                boolean_parameter("use_open_routing", default=False, help="Use OpenAI for routing"),
                text_parameter("Who is your daddy what what does he do?", default="a nerd!", help="Just answer the question..."),
                prompt_parameter("Generate node prompt", default="Initial remark...", help="The prompt for the generate node"),
                prompt_parameter("Reflect node prompt", default="back to back", help="The prompt for the reflect node"),
            ]
        }

    @classmethod
    # def build_graph(cls, use_open_routing: bool):
    def build_graph(cls):

        from src.constructs.test_graph.router import route_OpenAI, route_Ollama
        from src.constructs.test_graph.friendly_chatbot import friendly_chatbot
        from src.constructs.test_graph.vector_store import vectorstore


        # workflow = StateGraph(GraphState)
        graph_builder = StateGraph(State)


        graph_builder.add_node("vectorstore", vectorstore)
        graph_builder.add_edge("vectorstore", END)
        graph_builder.add_node("friendly_chatbot", friendly_chatbot)
        graph_builder.add_edge("friendly_chatbot", END)
        graph_builder.add_node("bad_route", bad_route)
        graph_builder.add_edge("bad_route", END)

        graph_builder.set_conditional_entry_point(
                        # route_OpenAI if use_open_routing else route_Ollama,
                        route_Ollama,
                        {
                            "vectorstore": "vectorstore",
                            "friendly_chatbot": "friendly_chatbot",
                            "bad_route": "bad_route"
                        }
                    )


        graph = graph_builder.compile()
        return graph



    # @classmethod
    # # def invoke_graph(self, bot_reply_placeholder, thoughts):
    # #     pass

    # async def run_graph(cls, thought_container, bot_reply_chatmessage, status_expander):

    #     # st.info("Running the graph...")

    #     graph_config = RunnableConfig()
    #     # st_callback = StreamlitCallbackHandler(answer_container)
    #     # st_callback = custom_callback(answer_container)
    #     # st_callback = custom_callback()
    #     # st_callback = MyCustomHandler()
    #     # st_callback = StreamlitCallbackHandler(st.container())
    #     # graph_config['callbacks'] = [st_callback]
    #     # graph_config['callbacks'] = [StreamingStdOutCallbackHandler()]
    #     # graph_config['callbacks'] = [callback()]
    #     graph_config['hyperparameters'] = st.session_state.graph_hyperparameters
    #     graph_config['metadata'] = {"conversation_id": st.session_state.session_id}
    #     # st.sidebar.markdown("# Graph config:")
    #     # st.sidebar.json(graph_config)

    #     graph_input = {"input": st.session_state.input, "messages": st.session_state.convo_history}
    #     # st.sidebar.markdown("# Graph input:")
    #     # st.sidebar.json(graph_input)

    #     # NOTE: we give parameters to the graph builder as it will be used to differentiate builds of the graph!!
    #     graph = cls.build_graph(use_open_routing=False)





    #     streamed_chunks = ""
    #     current_node = None
    #     # current_writer = None
    #     current_writer = bot_reply_chatmessage.empty()
    #     thought_writer = None
    #     async for event in graph.astream_events(
    #                             input=graph_input,
    #                             config=graph_config,
    #                             version='v1'
    #                         ):
    #         print(event)
    #         print('\n\n')
    #         # thought_text.json(event)
    #         status_expander.write(event['event'])
    #         status_expander.update(label=f":orange[Running:] :red[{event['event']}]")

    #         if event['event'] == "on_chain_end":
    #             if event['name'] == "LangGraph":
    #                 last_node = event['data']['output'].keys()
    #                 # print(last_node)
    #                 # get the first key
    #                 last_key = list(last_node)[0]
    #                 last_message = event['data']['output'].get(last_key)['messages'][0].content

    #         if event['event'] != current_node:
    #             streamed_chunks = ""
    #             current_node = event['event']
    #             # thought_container.write(f"Node: {current_node}")

    #             if current_node not in ["on_chat_model_stream", "on_llm_new_token"]:
    #                 continue

    #             # current_thought = thought_container.status(f"{current_node}", state="running", expanded=True)
    #             # with current_thought:
    #                 # thought_writer = st.empty()
    #             # if thought_writer:
    #                 # thought_writer.markdown("\n---\n")
    #             thought_writer = thought_container.empty()
    #             # thought_writer = thought_writer.container()
    #             # thought_writer.markdown("\n---\n")
    #             # thought_writer.write(f"Node: {current_node}")


    #         # feedback_type = event['metadata'].get('feedback_type', None)
    #         feedback_type = event['metadata'].get('UI_name', None)

    #         # AN LLM IS GIVING FEEDBACK TO THE USER!
    #         if feedback_type == "Friendly Chatbot":
    #             if event['data'].get('chunk', None):
    #                 streamed_chunks += event['data']['chunk'].content
    #                 current_writer.markdown(streamed_chunks)

    #                 # with current_writer:
    #                     # st.write(streamed_chunks)
    #                     # current_writer.update()


    #         if feedback_type == "Ollama Router":
    #             if event['data'].get('chunk', None):
    #                 streamed_chunks += event['data']['chunk'].content
    #                 thought_writer.code(streamed_chunks)

    #     st.session_state.convo_history.append(HumanMessage(content=st.session_state.input))
    #     st.session_state.convo_history.append(AIMessage(content=last_message))
