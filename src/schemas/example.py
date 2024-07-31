from pydantic import BaseModel

from langchain_core.prompts import (
    ChatPromptTemplate,
)


class Example(BaseModel):
    input: str
    output: str

    def get_example_prompt(self) -> ChatPromptTemplate:
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        return example_prompt
