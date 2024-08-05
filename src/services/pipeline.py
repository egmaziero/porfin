from typing import Union
from src.schemas.enums import RoleEnum
from src.schemas.message import Message
from src.services.config import Config
from src.prompts.prompts import Prompt
from src.services.vdb import VectorDataBase
from src.services.llm import LLM
from langchain_core.messages.ai import AIMessage


class Pipeline:
    def __init__(self, config: Config):
        self.prompter = Prompt(config)  # Responsible for creating the prompts
        self.vdb = VectorDataBase(config)  # Vector Database
        self.llm = LLM(config)  # Interactions with the LLM

    def execute(
        self, user_input: str, llm_model: str, n_examples: int
    ) -> Union[str, list]:
        # given a use input, get the examples
        examples = self.vdb.search(user_input, n_examples)
        # keep interactions in session
        last_used_examples = [
            {
                "User input": user_input,
                "Examples": [
                    {"input": e.metadata["input"], "output": e.metadata["output"]}
                    for e in examples
                ],
            }
        ]
        # prepare the few-shot prompt
        few_shot_prompt = self.prompter.get_few_shot_prompt(examples)
        # consult the model
        response: AIMessage = self.llm.get_response(
            few_shot_prompt, user_input, llm_model
        )
        # prepare Message
        message = Message(role=RoleEnum.ASSISTANT, content=response.content)
        return message, last_used_examples
