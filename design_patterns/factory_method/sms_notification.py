import requests

from design_patterns.factory_method.notification import Notification


class InvalidSinchResponse(Exception):
    pass


class SMSNotification(Notification):
    def __init__(self, service_plan_id: str | None = None,
                 api_token: str | None = None,
                 sinch_number: str | None = None,
                 to_number: str | None = None):
        self.service_plan_id = service_plan_id
        self.api_token = api_token
        self.sinch_number = sinch_number
        self.to_number = to_number

        self.url = "https://us.sms.api.sinch.com/xms/v1/"\
            f"{self.service_plan_id}/batches"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.api_token)
        }

    def send_notification(self) -> None:
        response = requests.post(self.url, json=self.payload,
                                 headers=self.headers)
        try:
            assert response.status_code == 200
        except AssertionError:
            raise InvalidSinchResponse(response.json())

    def set_message(self, message: str) -> None:
        self.payload = {
            "from": self.sinch_number,
            "to": [self.to_number],
            "body": message
        }
