from unittest.mock import patch
from uuid import uuid4

from design_patterns.dataclasses.sms_notification import SMSType
from design_patterns.factory_method.sms_notification import (
    SMSNotification,
    SMSNotificationError,
)

from tests.base_test_case import BaseTestCase


class TestSMSNotification(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('boto3.client')
    def test_send_notification(self, mock_client):
        mock_response = mock_client.return_value

        sms_notification = SMSNotification()
        message = "test_message"
        receiver_number = "333333"
        sms_type = SMSType.PROMOTIONAL

        expected_aws_response = {
            'MessageId': uuid4(),
            'ResponseMetadata': {
                'RequestId': uuid4(),
                'HTTPStatusCode': 200
            }
        }
        mock_response.publish.return_value = expected_aws_response

        sms_notification.send_notification(message, receiver_number, sms_type)

        expected_message_attributes = {
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': sms_notification.payload.sender
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': sms_type
            }
        }

        mock_response.publish.assert_called_once_with(
            PhoneNumber=sms_notification.payload.phone_number,
            Message=sms_notification.payload.message,
            MessageAttributes=expected_message_attributes)

    @patch('boto3.client')
    def test_send_notification_fails(self, mock_client):
        mock_response = mock_client.return_value
        mock_response.publish.side_effect = Exception()

        sms_notification = SMSNotification()
        message = "test_message"
        receiver_number = "333333"
        sms_type = SMSType.PROMOTIONAL

        with self.assertRaises(SMSNotificationError) as ctxt:
            sms_notification.send_notification(message,
                                               receiver_number,
                                               sms_type)
            assert ctxt.msg == \
                "There was an error while trying to send the SMS notification"
