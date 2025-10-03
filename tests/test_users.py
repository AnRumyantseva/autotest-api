from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from http import HTTPStatus
from tools.assertions.schema import validate_json_schema
from tools.assertions.basic import assert_status_code


def test_create_user():
    public_users_client = get_public_users_client()
    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert response_data.user.email == request.email, 'Некорректный email пользователя'
    assert response_data.user.last_name == request.last_name, 'Некорректный last_name пользователя'
    assert response_data.user.first_name == request.first_name, 'Некорректный first_name пользователя'
    assert response_data.user.middle_name == request.middle_name, 'Некорректный middle_name пользователя'
    validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
