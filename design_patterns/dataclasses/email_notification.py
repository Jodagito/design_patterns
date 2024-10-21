from pydantic.dataclasses import dataclass


@dataclass
class MessagePayload:
    html_template: str | None
    message: str
    receiver_emails: list[str]
    title: str
