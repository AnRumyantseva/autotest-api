from pydantic import BaseModel, HttpUrl


class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """
    id: str
    url: HttpUrl
    filename: str
    directory: str


class CreatedFileResponseSchema(BaseModel):
    file: FileSchema


class CreateFileRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание файла.
    """
    filename: str
    directory: str
    upload_file: str
