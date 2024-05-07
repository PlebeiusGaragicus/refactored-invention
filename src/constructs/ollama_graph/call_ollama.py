import logging
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain.prompts import PromptTemplate

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


from src.interface import Colors, cprint
from src.constructs.test_graph import State



def call_ollama(state: State, config: RunnableConfig):
    logging.debug("NODE: friendly_chatbot()")

    print(config)

    if config['hyperparameters']['llm_model'] != "OpenAI":
        llm = ChatOllama(model=config['hyperparameters']['llm_model'], temperature=0.8)

    messages = '\n'.join(f"{message.type}: {message.content}" for message in state["messages"])
    input = state["input"]

    prompt = PromptTemplate(
        template="""{behaviour}

---

{input}
""",
        input_variables=["messages"],
        partial_variables={"behaviour": config['hyperparameters']['Behaviour prompt']}
        )


    cprint(prompt.pretty_repr().format(input=input), Colors.CYAN)
    logging.debug(prompt.pretty_repr().format(input=input))

    chain = prompt | llm

    this_config = config
    this_config['metadata']['node_type'] = "output"

    bot_reply = chain.invoke({"input": input}, config=this_config)
    return {"messages": [AIMessage(content=bot_reply.content)]}
