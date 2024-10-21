from uuid import UUID

from pydantic import BaseModel, model_validator


class ResponseMetadata(BaseModel):
    request_id: UUID
    http_status_code: int


class AWSNotificationResponse(BaseModel):
    message_id: UUID
    response_metadata: ResponseMetadata

    @model_validator(mode='before')
    def unpack_json(cls, values) -> dict:
        message_id = values.get('MessageId')
        response_metadata = values.get('ResponseMetadata')

        if response_metadata:
            request_id = response_metadata.get('RequestId')
            http_status_code = response_metadata.get('HTTPStatusCode')

            values['message_id'] = message_id
            values['response_metadata'] = ResponseMetadata(
                request_id=request_id, http_status_code=http_status_code)

        return values
