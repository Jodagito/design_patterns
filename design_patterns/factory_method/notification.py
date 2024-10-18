from abc import (
    ABC,
    abstractmethod,
)


class Notification(ABC):
    @abstractmethod
    def send_notification(self) -> None:
        pass

    @abstractmethod
    def set_message(self, message: str) -> None:
        pass
