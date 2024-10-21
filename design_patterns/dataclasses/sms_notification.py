from enum import Enum

from pydantic.dataclasses import dataclass


class SMSType(Enum):
    PROMOTIONAL = "Promotional"
    TRANSACTIONAL = "Transactional"


@dataclass
class MessagePayload:
    message: str
    phone_number: str
    sender: str
