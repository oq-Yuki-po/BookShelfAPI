from pydantic import BaseModel, ConfigDict, Field


class GoogleBooksApiSaveOut(BaseModel):

    message: str = Field(title='message', min_length=1, max_length=255, default='book saved successfully')
    title: str = Field(title='title', min_length=1, max_length=255)
    authors: list = Field(title='authors', min_length=1, max_length=255)
    published_at: str = Field(title='published_at', min_length=1, max_length=255)
    cover_image_base64: str = Field(title='cover_image_base64', min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'message': 'book saved successfully',
                'title': 'sample title',
                'authors': ['sample author'],
                'published_at': '2021-01-01',
                'cover_image_base64': 'sample base64 string'
            }
        }
    )
