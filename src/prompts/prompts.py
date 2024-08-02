from src.schemas.example import Example

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)


class Prompt:
    def __init__(self, system_instructions: str) -> None:
        self.system_instructions = system_instructions

    def get_few_shot_prompt(self, examples: list[Example]) -> list[Example]:
        # examples = [
        #     {"input": "2+2", "output": "4"},
        #     {"input": "2+3", "output": "5"},
        # ]
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )
        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{self.system_instructions}"),
                few_shot_prompt,
                ("human", "{input}"),
            ]
        )
        return few_shot_prompt
