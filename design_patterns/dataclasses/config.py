from pydantic.dataclasses import dataclass


@dataclass
class Config:
    sinch_api_token: str
    sinch_number: str
    sinch_service_plan_id: str
    sinch_url: str
