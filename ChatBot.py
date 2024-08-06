from pathlib import Path
import streamlit as st

from src.schemas.message import Message
from src.schemas.enums import RoleEnum
from src.services.config import Config
from src.services.logger import Logger
from src.services.pipeline import Pipeline

# Path to data directory
DATA_PATH = Path(__file__).parents[0] / "src/data"
# Initialize the config utility
config = Config(config_file=DATA_PATH / "configs.json")
# Initialize the main pieces of the chatbot
pipeline = Pipeline(config)  # Main pipeline

logger = Logger(name="GUI").get_logger()

# Initialize the session state
session_variables = ["messages", "last_used_examples"]
for session_var in session_variables:
    if session_var not in st.session_state:
        st.session_state[session_var] = []


st.title(config.get("chat_bot_title"))
st.caption(config.get("chat_bot_description"))

with st.sidebar:
    st.header("Available LLMs")
    llm_model_name = st.selectbox(
        "Change", options=config.get("llm_model_name_alternatives")
    )  # this model name will be used when making a request to the pre-trained llm
    n_examples = st.number_input(
        "Number of examples", min_value=0, max_value=10, value=5
    )  # this is the number of examples to be used when creating the few-shot prompt
    st.header("Configuration")
    st.json(config.current(), expanded=False)  # shows the current configuration
    st.caption("Current configuration")
    st.header("Interactions")
    st.json(
        st.session_state.last_used_examples, expanded=False
    )  # list all last interactions with the model
    st.caption("Examples")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message.role.value):
        st.markdown(message.content)

if prompt := st.chat_input("Como posso te ajudar?"):
    # Add user message to chat history
    st.session_state.messages.append(Message(role=RoleEnum.USER, content=prompt))
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response, last_examples = pipeline.execute(prompt, llm_model_name, n_examples)
        st.session_state.last_used_examples.append(last_examples)
        st.write(response.content)
    # Add assistant response to chat history
    st.session_state.messages.append(
        Message(role=RoleEnum.ASSISTANT, content=response.content)
    )
