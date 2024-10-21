from dataclasses import asdict
from unittest.mock import patch
from uuid import uuid4

from design_patterns.dataclasses.push_notification import Platform
from design_patterns.factory_method.push_notification import (
    PushNotification,
    PushNotificationError,
)
from tests.base_test_case import BaseTestCase


class TestPushNotification(BaseTestCase):
    def setUp(self):
        super().setUp()

    @patch('boto3.client')
    def test_send_notification(self, mock_client):
        mock_response = mock_client.return_value

        push_notification = PushNotification(Platform.BROWSER)
        device_token = "test_token"
        body = "test_body"
        title = "test_title"

        expected_aws_response = {
            'MessageId': uuid4(),
            'ResponseMetadata': {
                'RequestId': uuid4(),
                'HTTPStatusCode': 200
            }
        }
        mock_response.publish.return_value = expected_aws_response

        push_notification.send_notification(device_token,
                                            body,
                                            title)

        mock_response.publish.assert_called_once_with(
            TargetArn=push_notification.endpoint_arn,
            MessageStructure='json',
            Message=asdict(push_notification.payload))

    @patch('boto3.client')
    def test_send_notification_fails(self, mock_client):
        mock_response = mock_client.return_value

        push_notification = PushNotification(Platform.BROWSER)
        device_token = "test_token"
        body = "test_body"
        title = "test_title"

        mock_response.publish.side_effect = Exception()

        with self.assertRaises(PushNotificationError) as ctxt:
            push_notification.send_notification(device_token,
                                                body,
                                                title)
            assert ctxt.msg == "Error while sending the push notification"

    @patch('boto3.client')
    def test_send_notification_fails_device_registration(self, mock_client):
        mock_response = mock_client.return_value

        push_notification = PushNotification(Platform.BROWSER)
        device_token = "test_token"
        body = "test_body"
        title = "test_title"

        mock_response.create_platform_endpoint.side_effect = Exception()

        with self.assertRaises(PushNotificationError) as ctxt:
            push_notification.send_notification(device_token,
                                                body,
                                                title)
            assert ctxt.msg == "Error while sending the push notification"
