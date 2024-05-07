import logging

from typing import Annotated, Literal

# from typing_extensions import TypedDict

# from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain.prompts import PromptTemplate

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from src.interface import Colors, cprint
from src.constructs.test_graph import State








# def route_question(state: State, config):
def route_Ollama(state: State, config: RunnableConfig):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    print("THIS IS THE STATE")
    print(state)

    state["something_random"] = 4494

    # cprint("\n--- NODE: route_Ollama() ---", Colors.MAGENTA)
    logging.debug("NODE: route_Ollama()")
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
    logging.debug(prompt.pretty_repr().format(question=question))
    # print(prompt.pretty_repr())
    # cprint(f"Convo History: {convo_history}", Colors.RED)
    # cprint(f"Question: {question}", Colors.RED)

    question_router = prompt | llm | JsonOutputParser()

    this_config = config
    this_config['metadata']['node_type'] = "thought"

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
    logging.debug("NODE: route_OpenAI()")
    # cprint("\n--- NODE: route_OpenAI() ---", Colors.MAGENTA)

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
    logging.debug(prompt.pretty_repr().format(question=question))

    question_router = prompt | structured_llm_router
    source = question_router.invoke({"question": question}, config=config)
    logging.debug(source.datasource)
    # cprint(source.datasource, Colors.GREEN)
    if source.datasource == 'vectorstore':
        print("---ROUTE QUESTION TO vectorstore---")
        return "vectorstore"
    elif source.datasource == 'friendly_chatbot':
        print("---ROUTE QUESTION TO friendly chatbot---")
        return "friendly_chatbot"
    else:
        print("---ROUTING ERROR---")
        return "bad_route"


