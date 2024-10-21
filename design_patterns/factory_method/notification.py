from abc import (
    ABC,
    abstractmethod,
)

import boto3

from design_patterns.singleton.config import ConfigsLoader


class Notification(ABC):
    def __init__(self, client: str):
        self.configs = ConfigsLoader().get_configs()
        self.payload: dict = None
        self.client = boto3.client(client, self.configs.aws_region)

    @abstractmethod
    def send_notification(self) -> None:
        pass

    @abstractmethod
    def _aws_client_handler(self) -> None:
        pass

    @abstractmethod
    def _set_message_payload(self) -> None:
        pass
