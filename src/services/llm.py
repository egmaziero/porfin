import os

from src.services.config import Config
from src.services.logger import Logger
from src.schemas.message import Message
from src.schemas.enums import RoleEnum

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage

logger = Logger(name="LLM").get_logger()


class LLM:

    def __init__(self, config: Config):

        os.environ["GROQ_API_KEY"] = config.get("llm_api_key")
        self.model = ChatGroq(model=config.get("llm_model_name"))
        logger.info("LLM started")

    def get_response(
        self, prompt: ChatPromptTemplate, input: str, llm_model_name: str = None
    ) -> Message:
        self.model = ChatGroq(model=llm_model_name)
        logger.info(f"Getting response from LLM. User input: {input}")
        chain = prompt | self.model
        response = chain.invoke({"user_input": input})
        logger.info(
            f"Response metadata received from LLM: {response.response_metadata}"
        )
        message = Message(role=RoleEnum.ASSISTANT, content=response.content)
        return message
