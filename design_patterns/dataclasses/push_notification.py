from enum import Enum

from pydantic.dataclasses import dataclass


class Platform(Enum):
    ANDROID = 'android'
    BROWSER = 'browser'
    IOS = 'ios'


@dataclass
class NotificationContent:
    body: str
    title: str


@dataclass
class APNSMessage:
    aps: NotificationContent
    sound: str


@dataclass
class GCMMessage:
    notification: NotificationContent


@dataclass
class MessagePayload:
    default: str | None = "You have a new notification!"
    APNS: APNSMessage | None = None
    GCM: GCMMessage | None = None
