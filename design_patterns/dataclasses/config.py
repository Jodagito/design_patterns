from pydantic.dataclasses import dataclass


@dataclass
class Config:
    sms_sender_number: str
    default_source_email: str
