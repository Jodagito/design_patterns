from pydantic.dataclasses import dataclass


@dataclass
class Config:
    aws_region: str
    sms_sender_number: str | None
    default_source_email: str | None
    android_application_arn: str | None
    browser_application_arn: str | None
    ios_application_arn: str | None
