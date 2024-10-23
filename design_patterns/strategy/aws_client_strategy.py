from abc import (
    ABC,
    abstractmethod,
)


class AWSClientStrategy(ABC):
    @abstractmethod
    def perform_operation(self):
        pass
