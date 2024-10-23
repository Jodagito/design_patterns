import boto3

from design_patterns.dataclasses.sms_notification import SMSType
from design_patterns.models.notification import AWSNotificationResponse
from design_patterns.strategy.aws_client_strategy import AWSClientStrategy


class SNSClientDirectStrategy(AWSClientStrategy):
    """It is used to send one SMS notification to one phone number."""

    client = boto3.client('sns')

    def perform_operation(self, phone_number: str,
                          message: str,
                          sender: str,
                          sms_type: SMSType) -> AWSNotificationResponse:
        response = self.client.publish(
            PhoneNumber=phone_number,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': sender
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': sms_type
                }
            }
        )
        return AWSNotificationResponse(**response)


class SNSClientTopicStrategy(SNSClientDirectStrategy):
    """It is used to send one push notification to multiple devices."""

    def perform_operation(self, endpoint_arn: str,
                          payload: dict) -> AWSNotificationResponse:
        response = self.client.publish(
            TargetArn=endpoint_arn,
            MessageStructure='json',
            Message=payload
        )
        return AWSNotificationResponse(**response)


class SNSClientPlatformStrategy(SNSClientDirectStrategy):
    """It is used to register one device token and generate an ARN."""

    def perform_operation(self, platform_arn: str, device_token: str) -> dict:
        return self.client.create_platform_endpoint(
            PlatformApplicationArn=platform_arn,
            Token=device_token
        )


class SNSClientStrategyContext:
    def __init__(self):
        self.sns_client_direct_strategy = SNSClientDirectStrategy()
        self.sns_client_topic_strategy = SNSClientTopicStrategy()
        self.sns_client_platform_strategy = SNSClientPlatformStrategy()
