from enum import Enum


class RoleEnum(str, Enum):
    """
    Roles for Message
    """

    ASSISTANT = "assistant"
    USER = "user"
