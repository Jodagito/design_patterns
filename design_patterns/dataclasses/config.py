from pydantic.dataclasses import dataclass


@dataclass
class Config:
    sms_sender_number: str
    smtp_server: str
    smtp_port: int
    smtp_login: str
    smtp_password: str
    default_smtp_email: str
