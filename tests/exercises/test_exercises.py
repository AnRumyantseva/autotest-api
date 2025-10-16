from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.basic import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.exercises
class TestExercises:
    def test_create_exercise(self, exercise_client: ExercisesClient, function_course: CourseFixture):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercise_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        response = exercise_client.get_exercise_api(exercise_id=function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(function_exercise.response, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        request = UpdateExerciseRequestSchema()
        response = exercise_client.update_exercise_api(exercise_id=function_exercise.response.exercise.id,
                                                       request=request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        response_delete = exercise_client.deleted_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(response_delete.status_code, HTTPStatus.OK)

        response_get = exercise_client.get_exercise_api(function_exercise.response.exercise.id)
        response_get_data = InternalErrorResponseSchema.model_validate_json(response_get.text)

        assert_status_code(response_get.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(response_get_data)
        validate_json_schema(response_get.json(), response_get_data.model_json_schema())
