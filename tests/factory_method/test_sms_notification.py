from unittest.mock import patch

from design_patterns.factory_method.sms_notification import (
    SMSNotification,
    SMSNotificationError,
)

from tests.base_test_case import BaseTestCase


class TestSMSNotification(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('requests.post')
    def test_send_message(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200

        sms_notification = SMSNotification()
        message = "test_message"
        sms_notification.set_message_payload(message, ["333333"])
        sms_notification.send_notification()

        mock_post.assert_called_once_with(sms_notification.url,
                                          json=sms_notification.payload,
                                          headers=sms_notification.headers)

    @patch('requests.post')
    def test_send_message_fails(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "test_error"}

        sms_notification = SMSNotification()
        message = "test_message"
        sms_notification.set_message_payload(message, "333333")

        with self.assertRaises(SMSNotificationError) as ctxt:
            sms_notification.send_notification()
            assert ctxt.msg == {"error": "test_error"}

    def test_set_message_payload(self):
        sms_notification = SMSNotification()
        message = "test_message"
        sms_notification.set_message_payload(message, "333333")
        assert sms_notification.payload["body"] == message
