import pytest
from http import HTTPStatus
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema
from tools.assertions.basic import assert_status_code


@pytest.mark.authentication
@pytest.mark.regression
class TestAuthentication:
    def test_login(self, authentication_client: AuthenticationClient, function_user: UserFixture):
        request_login = LoginRequestSchema(email=function_user.email,
                                           password=function_user.password)
        response_login = authentication_client.login_api(request_login)
        response_login_data = LoginResponseSchema.model_validate_json(response_login.text)

        assert_status_code(response_login.status_code, HTTPStatus.OK)
        assert_login_response(response_login_data)

        validate_json_schema(instance=response_login.json(), schema=response_login_data.model_json_schema())
