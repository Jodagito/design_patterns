import boto3

from design_patterns.strategy.aws_client_strategy import AWSClientStrategy
from design_patterns.models.notification import AWSNotificationResponse


class SESClientStrategy(AWSClientStrategy):
    client = boto3.client('ses')

    def perform_operation(self, default_source_email: str,
                          receiver_emails: list[str],
                          title: str,
                          message: str,
                          html_template: str) -> AWSNotificationResponse:
        response = self.client.send_email(
            Source=default_source_email,
            Destination={
                'ToAddresses': receiver_emails
            },
            Message={
                'Subject': {
                    'Data': title,
                },
                'Body': {
                    'Text': {
                        'Data': message
                    },
                    'Html': {
                        'Data': html_template
                    }
                }
            }
        )
        return AWSNotificationResponse(**response)
