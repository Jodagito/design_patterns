from unittest.mock import patch

from design_patterns.factory_method.email_notification import (
    EmailNotification,
    EmailNotificationError,
)
from tests.base_test_case import BaseTestCase


class TestEmailNotification(BaseTestCase):
    def setUp(self):
        super().setUp()

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        mock_server = mock_smtp.return_value.__enter__.return_value

        message = "Test message"
        receiver_emails = ["test_email@test.com"]

        email_notification = EmailNotification()
        email_notification.set_message_payload(message,
                                               receiver_emails)
        email_notification.send_notification()

        mock_server.sendmail.assert_called_once_with(
            self.configs.default_smtp_email, receiver_emails, message)

    @patch('smtplib.SMTP')
    def test_send_email_fails(self, mock_smtp):
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.sendmail.side_effect = EmailNotificationError(
            "Error while sending the email")

        message = "Test message"
        receiver_emails = ["test_email@test.com"]

        email_notification = EmailNotification()
        email_notification.set_message_payload(message,
                                               receiver_emails)

        with self.assertRaises(EmailNotificationError) as ctxt:
            email_notification.send_notification()
            assert ctxt.msg == "Error while sending the email"

    @patch('smtplib.SMTP')
    def test_send_email_without_payload(self, mock_smtp):
        email_notification = EmailNotification()

        with self.assertRaises(EmailNotificationError) as ctxt:
            email_notification.send_notification()
            assert ctxt.msg == "No message payload has been set"

    def test_set_message_payload(self):
        message = "Test message"
        receiver_emails = ["test_email@test.com"]

        email_notification = EmailNotification()
        email_notification.set_message_payload(message,
                                               receiver_emails)

        expected_payload = {"message": message,
                            "receiver_emails": receiver_emails}
        assert email_notification.payload == expected_payload
