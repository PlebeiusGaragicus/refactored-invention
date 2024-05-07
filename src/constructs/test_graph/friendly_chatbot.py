import logging
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain.prompts import PromptTemplate

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


from src.interface import Colors, cprint
from src.constructs.test_graph import State






def friendly_chatbot(state: State, config: RunnableConfig):
    logging.debug("NODE: friendly_chatbot()")
    # cprint("\n--- NODE: friendly_chatbot() ---", Colors.MAGENTA)

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
    logging.debug(prompt.pretty_repr().format(input=input))

    chain = prompt | llm

    this_config = config
    this_config['metadata']['node_type'] = "output"

    # return {"messages": [chain.invoke({"user_input": user_input, "messages": convo_history}, config=config)]}
    # return {"messages": [chain.invoke({"messages": messages}, config=this_config)]}
    bot_reply = chain.invoke({"input": input}, config=this_config)
    # return {"messages": [AIMessage(content=bot_reply)]}
    return {
        "messages": [AIMessage(content=bot_reply.content)],
        # "something_random": 123
        }
