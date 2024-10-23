from dataclasses import asdict

from design_patterns.dataclasses.aws_client_strategy import \
    AWSClientStrategyType
from design_patterns.dataclasses.push_notification import (
    APNSMessage,
    GCMMessage,
    MessagePayload,
    NotificationContent,
    Platform,
)
from design_patterns.factory_method.notification import Notification


class PushNotificationError(Exception):
    pass


class PushNotification(Notification):
    def __init__(self, platform: Platform):
        super().__init__(AWSClientStrategyType.SNS)
        self.platform = platform

    def send_notification(self, device_token: str, body: str,
                          title: str, sound: str | None = 'default') -> None:
        self._set_platform_application_arn()
        self._register_device(device_token)
        self._set_message_payload(body, title, sound)
        self._aws_client_handler()

    def _aws_client_handler(self) -> None:
        try:
            response = self.client.sns_client_topic_strategy.perform_operation(
                self.endpoint_arn,
                asdict(self.payload)
            )
            assert response.response_metadata.http_status_code == 200
        except Exception:
            raise PushNotificationError(
                "Error while sending the push notification")

    def _set_platform_application_arn(self) -> str:
        if self.platform == Platform.ANDROID:
            self.platform_arn = self.configs.android_application_arn
        elif self.platform == Platform.BROWSER:
            self.platform_arn = self.configs.browser_application_arn
        elif self.platform == Platform.IOS:
            self.platform_arn = self.configs.ios_application_arn

    def _register_device(self, device_token: str) -> None:
        try:
            response = self.client.sns_client_platform_strategy.\
                perform_operation(self.platform_arn, device_token)
            self.endpoint_arn = response['EndpointArn']
        except Exception:
            raise PushNotificationError(
                "Error while sending the push notification")

    def _set_message_payload(self, body: str, title: str,
                             sound: str | None) -> None:
        notification_content = NotificationContent(body=body, title=title)

        if self.platform == Platform.IOS:
            apns = APNSMessage(aps=notification_content,
                               sound=sound)
            self.payload = MessagePayload(APNS=apns)
        elif self.platform in [Platform.ANDROID, Platform.BROWSER]:
            gcm = GCMMessage(notification=notification_content)
            self.payload = MessagePayload(GCM=gcm)
