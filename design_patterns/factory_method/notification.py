from abc import (
    ABC,
    abstractmethod,
)

from design_patterns.singleton.config import ConfigsLoader


class Notification(ABC):
    def __init__(self):
        self.configs = ConfigsLoader().get_configs()

    @abstractmethod
    def send_notification(self) -> None:
        pass

    @abstractmethod
    def set_message_payload(self, message: str) -> None:
        pass
