from abc import (
    ABC,
    abstractmethod,
)

import boto3

from design_patterns.dataclasses.aws_client_strategy import \
    AWSClientStrategyType
from design_patterns.singleton.config import ConfigsLoader
from design_patterns.strategy.ses_client import SESClientStrategy
from design_patterns.strategy.sns_client import SNSClientStrategyContext


class Notification(ABC):
    def __init__(self, client: AWSClientStrategyType):
        self.payload: dict = None
        self.configs = ConfigsLoader().get_configs()
        if client == AWSClientStrategyType.SNS:
            self.client = SNSClientStrategyContext()
        elif client == AWSClientStrategyType.SES:
            self.client = SESClientStrategy()
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
