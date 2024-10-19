from pydantic.dataclasses import dataclass


@dataclass
class Config:
    sinch_api_token: str
    sinch_number: str
    sinch_service_plan_id: str
    sinch_url: str
    smtp_server: str
    smtp_port: int
    smtp_login: str
    smtp_password: str
    default_smtp_email: str
