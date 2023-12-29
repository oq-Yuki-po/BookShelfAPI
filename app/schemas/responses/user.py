from pydantic import BaseModel, Field


class UserSaveOut(BaseModel):

    message: str = Field(title='message', min_length=1, max_length=255, default='user saved successfully')

    class ConfigDict:
        json_schema_extra = {
            'example': {
                'message': 'user saved successfully'
            }
        }


class UserLoginOut(BaseModel):

    token: str = Field(title='token', min_length=1, max_length=255)
    type: str = Field(title='type', min_length=1, max_length=255, default='bearer')

    class ConfigDict:
        json_schema_extra = {
            'example': {
                'token': 'token',
                'type': 'bearer'
            }
        }
