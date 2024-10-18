from pydantic.dataclasses import dataclass


@dataclass
class Config:
    database_host: str
    database_user: str
    database_password: str
    database_port: str
    database_name: str
