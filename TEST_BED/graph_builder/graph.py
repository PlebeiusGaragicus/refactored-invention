import uuid

from typing import Annotated, Literal

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain.prompts import PromptTemplate

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from .interface import Colors, color, reset_color, cprint



# workflow = StateGraph(GraphState)

class State(TypedDict):
    input: str
    messages: Annotated[list, add_messages]




# Data model
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "friendly_chatbot"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

def route_OpenAI(state: State, config: RunnableConfig):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    cprint("\n--- NODE: route_OpenAI() ---", Colors.MAGENTA)

    question = state["messages"][-1].content
    # messages = '\n'.join(f"{message.type}: {message.content}" for message in state["messages"])


    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, streaming=True)
    structured_llm_router = llm.with_structured_output(RouteQuery)


    system = """You are an expert at routing a user question to the next appropriate workflow:
Use 'vectorstore' for all questions related to firefighting: operations, policies, terminology, benefits, etc.
Use 'friendly_chatbot' for other user questions and/or small-talk.
You do not need to be stringent with the keywords in the question related to these topics.
Give a single choice based on the question.
Return JSON with a single key 'datasource' and no premable or explaination.\n
User question: {question}"""
    # p = [
    #     ("system", system),
    #     ("messages", state['messages'][-1].content)
    # ]
    # for message in state["messages"]:
        # p.append((message.type, message.content))
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
        ])

    cprint(prompt.pretty_repr().format(question=question), Colors.CYAN)

    question_router = prompt | structured_llm_router
    source = question_router.invoke({"question": question}, config=config)
    cprint(source.datasource, Colors.GREEN)
    if source.datasource == 'vectorstore':
        print("---ROUTE QUESTION TO vectorstore---")
        return "vectorstore"
    elif source.datasource == 'friendly_chatbot':
        print("---ROUTE QUESTION TO friendly chatbot---")
        return "friendly_chatbot"
    else:
        print("---ROUTING ERROR---")
        return "bad_route"


# def route_question(state: State, config):
def route_Ollama(state: State, config: RunnableConfig):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    print(state)

    cprint("\n--- NODE: route_Ollama() ---", Colors.MAGENTA)
    # convo_history = state["messages"][:-1]
    # question = state["messages"][-1].content
    question = state["input"]
    # messages = '\n'.join(f"{message.type}: {message.content}" for message in state["messages"])
    # print(convo_history)


    # model = "llama3:8b"
    # model = "mistral:7b"
    # model = "gemma:2b" # FUCKING SUCKS FOR ROUTING
    model = "gemma:7b" # FUCKING SUCKS FOR ROUTING
    llm = ChatOllama(model=model, format="json", temperature=0, num_predict=20)

    prompt = PromptTemplate(
        template="""You are an expert at routing a user question to the next appropriate workflow:
Use 'vectorstore' for all questions related to firefighting: operations, policies, terminology, benefits, etc.
Use 'friendly_chatbot' for other user questions and/or small-talk.
You do not need to be stringent with the keywords in the question related to these topics.
Give a single choice based on the user's question.
Return JSON with a single key 'datasource' and no premable, explaination or extra characters.
---
User question: {question}
""",
        # input_variables=["convo_history", "question"],
        input_variables=["question"],
    )
# Conversation history: {convo_history} \n
# User question: {question}

    # prompt.pretty_print()
    # cprint(prompt.pretty_repr().format(convo_history=convo_history, question=question), Colors.CYAN)
    cprint(prompt.pretty_repr().format(question=question), Colors.CYAN)
    # print(prompt.pretty_repr())
    # cprint(f"Convo History: {convo_history}", Colors.RED)
    # cprint(f"Question: {question}", Colors.RED)

    question_router = prompt | llm | JsonOutputParser()

    this_config = config
    this_config['metadata']['UI_name'] = "Ollama Router"

    # source = question_router.invoke({"convo_history": convo_history, "question": question}, config=config)
    # source = question_router.invoke({"messages": messages}, config=config)
    source = question_router.invoke({"question": question}, config=this_config)
    if source['datasource'] == 'vectorstore':
        print(">>> ROUTE QUESTION TO vectorstore")
        return "vectorstore"
    elif source['datasource'] == 'friendly_chatbot':
        print(">>> ROUTE QUESTION TO friendly chatbot")
        return "friendly_chatbot"
    else:
        print(">>> ROUTING ERROR")
        return "bad_route"





def friendly_chatbot(state: State, config: RunnableConfig):
    cprint("\n--- NODE: friendly_chatbot() ---", Colors.MAGENTA)

    print(config)

    if config['hyperparameters']['llm_model'] != "OpenAI":
        # model="llama3" # TODO - pull the model, temperature, etc from the config!
        # model = "gemma:2b" # Very fast!!
        llm = ChatOllama(model=config['hyperparameters']['llm_model'], temperature=0.8)
    else:
        # model = "gpt-3.5-turbo"
        # llm = ChatOpenAI(model=model, temperature=0.8)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)

    # user_input = state["messages"][-1].content
    # convo_history = state["messages"][:-1]
    # user_input = state["messages"][-1].content
    # messages = state["messages"]

    # format the message history for the prompt
    messages = '\n'.join(f"{message.type}: {message.content}" for message in state["messages"])
    input = state["input"]


            # Keep replies short, don't use proper grammar or punctuation.\n
    prompt = PromptTemplate(
#             template="""You are an human having an informal conversation with a friend.
# Your reply should be very short. Don't use proper syntax and punctuation.
# Don't be apologetic. Use emoji sparingly.
# If I don't say much, don't try to fill in the conversation.
            template="""You are an assistant.  Apologize to the user - their query didn't work.
Your reply should be very short.

User query:
{input}
""",
            input_variables=["messages"],
        )
            # Conversation history: {messages}\n
            # Your friend said: {user_input}""",
            # input_variables=["user_input", "messages"],
        
    cprint(prompt.pretty_repr().format(input=input), Colors.CYAN)

    chain = prompt | llm

    this_config = config
    this_config['metadata']['UI_name'] = "Friendly Chatbot"

    # return {"messages": [chain.invoke({"user_input": user_input, "messages": convo_history}, config=config)]}
    # return {"messages": [chain.invoke({"messages": messages}, config=this_config)]}
    bot_reply = chain.invoke({"input": input}, config=this_config)
    # return {"messages": [AIMessage(content=bot_reply)]}
    return {"messages": [AIMessage(content=bot_reply.content)]}


def vectorstore(state: State, config: RunnableConfig):
    cprint("\n--- NODE: vectorstore() ---", Colors.MAGENTA)

    return {"messages": [AIMessage(content="THE DATABASE IS NOT YET IMPLEMENTED!")]}


def bad_route(state: State, config: RunnableConfig):
    cprint("\n--- NODE: bad_route() ---", Colors.MAGENTA)
    cprint("### THIS SHOULD NEVER HAPPEN!!! ###", Colors.RED)

    return {"messages": [AIMessage(content="I'm sorry, I don't understand that question.")]}



def build_graph(use_open_routing: bool):
    graph_builder = StateGraph(State)

    graph_builder.add_node("vectorstore", vectorstore)
    graph_builder.add_edge("vectorstore", END)
    graph_builder.add_node("friendly_chatbot", friendly_chatbot)
    graph_builder.add_edge("friendly_chatbot", END)
    graph_builder.add_node("bad_route", bad_route)
    graph_builder.add_edge("bad_route", END)

    graph_builder.set_conditional_entry_point(
                    route_OpenAI if use_open_routing else route_Ollama,
                    {
                        "vectorstore": "vectorstore",
                        "friendly_chatbot": "friendly_chatbot",
                        "bad_route": "bad_route"
                    }
                )


    graph = graph_builder.compile()
    return graph



def graph_parameter_widgets():
    from .interface import create_slider, create_selectbox, create_checkbox, create_text_area

    # MODEL_OPTIONS = ['llama3:latest', 'mistral:7b', 'dolphin-mistral:latest', 'gemma:2b', 'OpenAI']
    MODEL_OPTIONS = ['gemma:2b', 'mistral:7b', 'dolphin-mistral:latest', 'OpenAI']


    return {
        "graph_name": "Example Graph",
        "widgets": [
            create_slider("llm_temperature", 0.0, 1.0, default=0.8),
            create_selectbox("llm_model", MODEL_OPTIONS),
            create_checkbox("use_open_routing", default=False),
            # create_text_area("remarks", default="Initial remark...")
            # create_text_area("wooske", default="back to back"),
        ]
    }
