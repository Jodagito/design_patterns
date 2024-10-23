from design_patterns.dataclasses.email_notification import MessagePayload
from design_patterns.factory_method.notification import Notification


class EmailNotificationError(Exception):
    pass


class EmailNotification(Notification):
    def __init__(self) -> None:
        super().__init__('ses')

    def send_notification(self, message: str,
                          receiver_emails: list[str],
                          title: str,
                          html_template_path: str | None = None) -> None:
        html_template = None
        if html_template_path:
            html_template = self._load_html_template(html_template_path)

        self._set_message_payload(message, receiver_emails, title,
                                  html_template)
        self._aws_client_handler()

    def _aws_client_handler(self) -> None:
        try:
            response = self.client.perform_operation(
                self.configs.default_source_email,
                self.payload.receiver_emails, self.payload.title,
                self.payload.message, self.payload.html_template)
            assert response.response_metadata.http_status_code == 200
        except Exception:
            raise EmailNotificationError(
                "There was an error while sending the email notification")

    def _set_message_payload(self, message: str,
                             receiver_emails: list[str],
                             title: str,
                             html_template: str | None) -> None:
        self.payload = MessagePayload(html_template=html_template,
                                      message=message,
                                      receiver_emails=receiver_emails,
                                      title=title)

    def _load_html_template(self, html_template_path) -> str:
        try:
            with open(html_template_path, 'r') as html_file:
                return html_file.read()
        except Exception as e:
            EmailNotificationError(e)
