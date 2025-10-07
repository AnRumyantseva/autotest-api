from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from http import HTTPStatus
import pytest
from tools.assertions.schema import validate_json_schema
from tools.assertions.basic import assert_status_code
from tools.assertions.users import assert_create_user


@pytest.mark.users
@pytest.mark.regression
def test_create_user():
    public_users_client = get_public_users_client()
    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user(request, response_data)
    validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())


@pytest.mark.slow
@pytest.mark.test
def test_heavy_calculation():
    pass

@pytest.mark.integration
@pytest.mark.test
def test_integration_with_external_api():
    pass

@pytest.mark.smoke
@pytest.mark.test
def test_quick_check():
    pass