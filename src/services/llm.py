import os

os.environ["GROQ_API_KEY"] = (
    "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"  # getpass.getpass()
)
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

model = ChatGroq(model="llama3-8b-8192")


class LLM:

    def __init__(self):
        self.store = {}

    def get_response(self, prompt: ChatPromptTemplate, input: str) -> AIMessage:
        chain = prompt | model
        response = chain.invoke({"input": f"{input}"})

        return response
