from langchain.memory import ChatMessageHistory


from langchain_core.runnables.history import RunnableWithMessageHistory

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)