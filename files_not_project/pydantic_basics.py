"""
{
  "id": "string",
  "title": "string",
  "maxScore": 0,
  "minScore": 0,
  "description": "string",
  "previewFile": {
    "id": "string",
    "filename": "string",
    "directory": "string",
    "url": "https://example.com/"
  },
  "estimatedTime": "string",
  "createdByUser": {
    "id": "string",
    "email": "user@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
  }
}
"""

from pydantic import BaseModel, Field, ConfigDict, computed_field, HttpUrl, EmailStr, ValidationError
from pydantic.alias_generators import to_camel
import uuid


class FileSchema(BaseModel):
    id: str
    url: HttpUrl
    filename: str
    directory: str


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    @computed_field(alias="username")
    def username(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    def get_username(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CoursesSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = 'Playwright'
    max_score: int = Field(alias='maxScore', default=1000)
    min_score: int = Field(alias='minScore', default=10)
    preview_file: FileSchema = Field(alias="previewFile")
    description: str = 'Playwright'
    estimated_time: str = Field(alias='estimatedTime', default='2 weeks')
    created_by_user: UserSchema = Field(alias="createdByUser")


course_default_model = CoursesSchema(
    id='course-id',
    title='Playwright',
    maxScore=100,
    minScore=10,
    previewFile=FileSchema(
        id="file-id",
        url="http://localhost:8000",
        filename="file.png",
        directory="courses",
    ),
    description='Playwright',
    estimatedTime='1 week',
    createdByUser=UserSchema(
        id="user-id",
        email="user@gmail.com",
        lastName="Bond",
        firstName="Zara",
        middleName="Alise"
    )
)
print('Course default model: ', course_default_model)

course_dict = {
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "previewFile": {
        "id": "file-id",
        "url": "http://localhost:8000",
        "filename": "file.png",
        "directory": "courses"
    },
    "description": "Playwright",
    "estimatedTime": "1 week",
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alise"
    }
}

course_dict_model = CoursesSchema(**course_dict)
print('Course dict model:', course_dict_model)

course_json = """
{
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "previewFile": {
        "id": "file-id",
        "url": "http://localhost:8000",
        "filename": "file.png",
        "directory": "courses"
    },
    "description": "Playwright",
    "estimatedTime": "1 week",
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alise"
    }
}
"""

course_json_model = CoursesSchema.model_validate_json(course_json)
print('Course JSON model:', course_json_model)

print(course_json_model.model_dump(by_alias=True))
print(course_json_model.model_dump_json(by_alias=True))

# course1 = CoursesSchema()
# print(course1)
# course2 = CoursesSchema()
# print(course2)


user = UserSchema(
    id="user-id",
    email="xhsuahx@hghj.com",
    lastName="Bond",
    firstName="Zara",
    middleName="Alise"
)
print(user.get_username())

print(user.username)
try:
    file = FileSchema(
        id="file-id",
        url="localhost",
        filename="file.png",
        directory="courses",
    )
except ValidationError as error:
    print(error)
    print(error.errors())
