from pydantic.dataclasses import dataclass


@dataclass
class Config:
    aws_region: str
    sms_sender_number: str
    default_source_email: str
