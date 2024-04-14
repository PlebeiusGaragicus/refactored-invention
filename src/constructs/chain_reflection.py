import asyncio
from typing import Sequence

from langchain_community.callbacks import StreamlitCallbackHandler

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI

from typing import List, Sequence

from langgraph.graph import END, MessageGraph

from pydantic import BaseModel

import streamlit as st

DEFAULT_GOAL = """You are an essay assistant tasked with writing excellent 5-paragraph essays.
Generate the best essay possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempts."""

DEFAULT_REFLECTION = """You are a teacher grading an essay submission. Generate critique and recommendations for the user's submission.
Provide detailed recommendations, including requests for length, depth, style, etc."""






class ChainReflectionBot():
    name: str = "Reflection"
    avatar: str = "🤔"


    def show_prompts(self):
        # st.text_area("SYSTEM", key="system_prompt", height=150, value=SYSTEM_PROMPT)
        st.text_area("Goal Prompt", key="goal_prompt", height=150, value=DEFAULT_GOAL)
        st.text_area("Reflection Prompt", key="reflection_prompt", height=150, value=DEFAULT_REFLECTION)
        st.write("Generate a short essay on the topicality of The Little Prince and its message in modern life. Keep it no more than 200 words.")


    def show_settings(self):
        # st.selectbox("Model", ["dolphin-mistral:latest", "mistral:7b", "llama2:7b", "gemma:2b"], key="selected_model")
        # st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="temperature")
        # st.number_input("Max Iterations", min_value=1, max_value=10, value=3, step=1, key="max_iterations")
        st.select_slider("Max Iterations", options=[i + 1 for i in range(10)], value=3, key="max_iterations")



        


    def run_prompt(self, bot_reply_placeholder):
        stream_handler = StreamlitCallbackHandler(bot_reply_placeholder, collapse_completed_thoughts=True)
        graph = compile_runnable(stream_handler)

        # return graph.stream([HumanMessage(content=st.session_state.prompt)],)

        async def update_UI():
            # yield graph.astream([HumanMessage(content=st.session_state.prompt)],)
            return graph.astream([HumanMessage(content=st.session_state.prompt)],)

        return asyncio.run(update_UI())



def compile_runnable(stream_handler):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                st.session_state.goal_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])
    generate = prompt | llm



    reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            st.session_state.reflection_prompt, # This is a 2-tuple of (role, content) with role being 'human', 'user', 'ai', 'assistant', or 'system'.
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])
    reflect = reflection_prompt | llm




    async def generation_node(state: Sequence[BaseMessage]):
        return await generate.ainvoke({"messages": state})


    async def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
        # Other messages we need to adjust
        cls_map = {"ai": HumanMessage, "human": AIMessage}
        # First message is the original user request. We hold it the same for all nodes
        translated = [messages[0]] + [
            cls_map[msg.type](content=msg.content) for msg in messages[1:]
        ]
        res = await reflect.ainvoke({"messages": translated})
        # We treat the output of this as human feedback for the generator
        return HumanMessage(content=res.content)


    builder = MessageGraph()
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.set_entry_point("generate")


    def should_continue(state: List[BaseMessage], max_iterations: int = 3):
        if len(state) / 2 > max_iterations: # TODO... hmmm
            return END
        return "reflect"


    builder.add_conditional_edges("generate", should_continue)
    builder.add_edge("reflect", "generate")
    graph = builder.compile() # returns a Pregel
    return graph
