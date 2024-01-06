from pydantic import BaseModel, ConfigDict, Field


class UserSaveOut(BaseModel):

    message: str = Field(title='message', min_length=1, max_length=255, default='user saved successfully')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'message': 'user saved successfully'
            }
        }
    )


class UserLoginOut(BaseModel):

    access_token: str = Field(title='token', min_length=1, max_length=255)
    type: str = Field(title='type', min_length=1, max_length=255, default='bearer')
    role: str = Field(title='role', min_length=1, max_length=255, default='user')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'access_token': 'token',
                'type': 'bearer',
                'role': 'user'
            }
        }
    )


class UserGetMeOut(BaseModel):

    user_name: str = Field(title='user name', min_length=1, max_length=255)
    role: str = Field(title='role', min_length=1, max_length=255, default='user')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'user_name': 'user name',
                'role': 'user'
            }
        }
    )
