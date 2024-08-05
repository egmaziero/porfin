from src.schemas.example import Example
from src.services.config import Config
from src.services.logger import Logger

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

logger = Logger(name="Prompter").get_logger()


class Prompt:
    def __init__(self, config: Config) -> None:
        logger.info("Starting Prompter...")
        self.system_instructions = config.get("system_instructions")
        logger.info("Prompter started")

    def get_few_shot_prompt(self, examples: list[Example]) -> ChatPromptTemplate:
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        dict_examples = [
            {"input": e.metadata["input"], "output": e.metadata["output"]}
            for e in examples
        ]
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=dict_examples,
        )
        logger.info(f"Few shot prompt created: {few_shot_prompt.format()}")
        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{self.system_instructions}"),
                few_shot_prompt,
                ("human", "{user_input}"),
            ]
        )
        return final_prompt
