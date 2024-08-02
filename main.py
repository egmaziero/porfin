import multiprocessing
from pathlib import Path
import streamlit as st
from langchain_core.messages.ai import AIMessage

from src.prompts.prompts import Prompt
from src.services.vdb import VectorDataBase
from src.services.llm import LLM


DATASET_PATH = Path(__file__).parents[0] / "src/data"

with open(DATASET_PATH / "system_instructions.txt", "r") as sys_instruct:
    prompter = Prompt(sys_instruct.read())
vdb = VectorDataBase()
llm = LLM()


def get_response(user_input: str) -> str:
    # given a use input, get the examples
    examples = vdb.search(user_input)
    # prepare the few-shot prompt
    few_shot_prompt = prompter.get_few_shot_prompt(examples)
    # consult the model
    response: AIMessage = llm.get_response(few_shot_prompt, user_input)

    return response


st.title("Home Scholling Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso te ajudar hoje?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    multiprocessing.freeze_support()
