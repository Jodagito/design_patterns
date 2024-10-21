from unittest.mock import patch
from uuid import uuid4

from design_patterns.factory_method.email_notification import (
    EmailNotification,
    EmailNotificationError,
)
from tests.base_test_case import BaseTestCase


class TestEmailNotification(BaseTestCase):
    def setUp(self):
        super().setUp()

    @patch('boto3.client')
    def test_send_email(self, mock_client):
        mock_response = mock_client.return_value

        email_notification = EmailNotification()
        message = "Test message"
        receiver_emails = ["test_email@test.com"]
        title = "Test Subject"

        expected_aws_response = {
            'MessageId': uuid4(),
            'ResponseMetadata': {
                'RequestId': uuid4(),
                'HTTPStatusCode': 200
            }
        }
        mock_response.send_email.return_value = expected_aws_response

        email_notification.send_notification(message, receiver_emails, title)

        expected_destination = {
            'ToAddresses': receiver_emails
        }
        expected_message = {
            'Subject': {
                'Data': title,
            },
            'Body': {
                'Text': {
                    'Data': message
                },
                'Html': {
                    'Data': None
                }
            }
        }

        mock_response.send_email.assert_called_once_with(
            Source=self.configs.default_source_email,
            Destination=expected_destination, Message=expected_message)

    @patch('boto3.client')
    def test_send_email_fails(self, mock_client):
        mock_response = mock_client.return_value
        mock_response.send_email.side_effect = Exception()

        email_notification = EmailNotification()
        message = "Test message"
        receiver_emails = ["test_email@test.com"]
        title = "Test Subject"

        with self.assertRaises(EmailNotificationError) as ctxt:
            email_notification.send_notification(message, receiver_emails,
                                                 title)
            assert ctxt.msg == \
                "There was an error while sending the email notification"
