import smtplib

from design_patterns.factory_method.notification import Notification


class EmailNotificationError(Exception):
    pass


class EmailNotification(Notification):
    def __init__(self) -> None:
        super().__init__()
        self.smtp_server: str = self.configs.smtp_server
        self.smtp_port: int = self.configs.smtp_port
        self.smtp_login: str = self.configs.smtp_login
        self.smtp_password: str = self.configs.smtp_password
        self.default_smtp_email: str = self.configs.default_smtp_email

    def send_notification(self) -> None:
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(self.smtp_login, self.smtp_password)
            if not self.payload:
                raise EmailNotificationError("No message payload has been set")
            try:
                server.sendmail(self.default_smtp_email,
                                self.payload.get('receiver_emails'),
                                self.payload.get('message'))
            except Exception as e:
                raise EmailNotificationError(e)

    def set_message_payload(self, message: str,
                            receiver_emails: list[str]) -> None:
        self.payload = {"message": message, "receiver_emails": receiver_emails}
