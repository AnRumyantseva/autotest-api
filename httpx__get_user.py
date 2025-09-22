import httpx
from tools.fakers import get_random_email

create_user_payload = {
  "email": get_random_email(),
  "password": "string123",
  "lastName": "string123",
  "firstName": "string123",
  "middleName": "string123"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json = create_user_payload)
print(create_user_response.json())
print(create_user_response.status_code)
create_user_data = create_user_response.json()
print("Create data:", create_user_data)


login_payload = {
  "email": create_user_payload['email'],
  "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_data_response = login_response.json()
print("Login data response:", login_data_response)


get_user_headers = {"Authorization" : f"Bearer {login_data_response['token']['accessToken']}"}
get_user_response = httpx.get(f"http://localhost:8000/api/v1/users/{create_user_data['user']['id']}", headers=get_user_headers)
print(get_user_response.request.url)
get_user_response_data = get_user_response.json()
print("Get user data:", get_user_response_data)
