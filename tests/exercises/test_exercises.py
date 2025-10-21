from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity
from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.basic import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory


@pytest.mark.regression
@pytest.mark.exercises
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.suite(AllureFeature.EXERCISES)
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.suitec(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create exercise")
    def test_create_exercise(self, exercise_client: ExercisesClient, function_course: CourseFixture):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercise_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get exercise")
    def test_get_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        response = exercise_client.get_exercise_api(exercise_id=function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(function_exercise.response, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Update exercise")
    def test_update_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        request = UpdateExerciseRequestSchema()
        response = exercise_client.update_exercise_api(exercise_id=function_exercise.response.exercise.id,
                                                       request=request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Delete exercise")
    def test_delete_exercise(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture):
        response_delete = exercise_client.deleted_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(response_delete.status_code, HTTPStatus.OK)

        response_get = exercise_client.get_exercise_api(function_exercise.response.exercise.id)
        response_get_data = InternalErrorResponseSchema.model_validate_json(response_get.text)

        assert_status_code(response_get.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(response_get_data)
        validate_json_schema(response_get.json(), response_get_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.tag(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get exercises")
    def test_get_exercises(self, exercise_client: ExercisesClient, function_exercise: ExerciseFixture,
                           function_course: CourseFixture):
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        response = exercise_client.get_exercises_api(query=query)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(response_data, [function_exercise.response])
        validate_json_schema(response.json(), response_data.model_json_schema())
