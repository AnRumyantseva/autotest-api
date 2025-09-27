"""
{
  "id": "string",
  "title": "string",
  "maxScore": 0,
  "minScore": 0,
  "description": "string",
  "estimatedTime": "string"
}
"""
from pydantic import BaseModel


class CoursesSchema(BaseModel):
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str


course_default_model = CoursesSchema(
    id ='course-id',
    title='Playwright',
    maxScore=100,
    minScore=10,
    description='Playwright',
    estimatedTime='1 week'
)