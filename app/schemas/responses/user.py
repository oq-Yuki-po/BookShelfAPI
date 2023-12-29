from pydantic import BaseModel, Field


class UserSaveOut(BaseModel):

    message: str = Field(title='message', min_length=1, max_length=255, default='user saved successfully')

    class Config:
        json_schema_extra = {
            'example': {
                'message': 'user saved successfully'
            }
        }


class UserLoginOut(BaseModel):

    access_token: str = Field(title='token', min_length=1, max_length=255)
    type: str = Field(title='type', min_length=1, max_length=255, default='bearer')
    role: str = Field(title='role', min_length=1, max_length=255, default='user')

    class Config:
        json_schema_extra = {
            'example': {
                'access_token': 'token',
                'type': 'bearer',
                'role': 'user'
            }
        }
