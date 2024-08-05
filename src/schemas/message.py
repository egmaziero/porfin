from pydantic import BaseModel
from src.schemas.enums import RoleEnum


class Message(BaseModel):
    role: RoleEnum
    content: str
