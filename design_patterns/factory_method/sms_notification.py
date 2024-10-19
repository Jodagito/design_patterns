import requests

from design_patterns.factory_method.notification import Notification


class SMSNotificationError(Exception):
    pass


class SMSNotification(Notification):
    def __init__(self):
        super().__init__()
        self.sinch_service_plan_id: str = self.configs.sinch_service_plan_id
        self.sinch_api_token: str = self.configs.sinch_api_token
        self.sinch_number: str = self.configs.sinch_number

        self.url: str = self.configs.sinch_url.format(
            sinch_service_plan_id=self.sinch_service_plan_id)
        self.headers: dict = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.sinch_api_token}"
        }

    def send_notification(self) -> None:
        response = requests.post(self.url, json=self.payload,
                                 headers=self.headers)
        try:
            assert response.status_code == 200
        except AssertionError:
            raise SMSNotificationError(response.json())

    def set_message_payload(self, message: str,
                            receiver_numbers: list[str]) -> None:
        self.payload = {
            "from": self.sinch_number,
            "to": receiver_numbers,
            "body": message
        }
