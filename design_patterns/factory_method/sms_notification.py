from design_patterns.dataclasses.aws_client_strategy import \
    AWSClientStrategyType
from design_patterns.dataclasses.sms_notification import (
    MessagePayload,
    SMSType,
)
from design_patterns.factory_method.notification import Notification


class SMSNotificationError(Exception):
    pass


class SMSNotification(Notification):
    def __init__(self):
        super().__init__(AWSClientStrategyType.SNS)

    def send_notification(self, message: str,
                          receiver_number: str,
                          sms_type: SMSType) -> None:
        self._set_message_payload(message, receiver_number)
        self._aws_client_handler(sms_type)

    def _aws_client_handler(self, sms_type: SMSType) -> None:
        try:
            response = self.client.sns_client_direct_strategy.\
                perform_operation(self.payload.phone_number,
                                  self.payload.message,
                                  self.payload.sender,
                                  sms_type)
            assert response.response_metadata.http_status_code == 200
        except Exception:
            raise SMSNotificationError(
                "There was an error while trying to send the SMS notification")

    def _set_message_payload(self, message: str, receiver_number: str) -> None:
        self.payload = MessagePayload(
            message=message,
            phone_number=receiver_number,
            sender=self.configs.sms_sender_number
        )
