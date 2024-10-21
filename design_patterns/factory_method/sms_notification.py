from design_patterns.dataclasses.sms_notification import (
    MessagePayload,
    SMSType,
)
from design_patterns.factory_method.notification import Notification
from design_patterns.models.notification import AWSNotificationResponse


class SMSNotificationError(Exception):
    pass


class SMSNotification(Notification):
    def __init__(self):
        super().__init__('sns')

    def send_notification(self, message: str,
                          receiver_number: str,
                          sms_type: SMSType) -> None:
        self._set_message_payload(message, receiver_number)
        self._aws_client_handler(sms_type)

    def _aws_client_handler(self, sms_type: SMSType) -> None:
        try:
            response = self.client.publish(
                PhoneNumber=self.payload.phone_number,
                Message=self.payload.message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': self.payload.sender
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': sms_type
                    }
                }
            )
            response = AWSNotificationResponse(**response)
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
