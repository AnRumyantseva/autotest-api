import httpx
from tools.fakers import get_random_email

create_user_payload = {
  "email": get_random_email(),
  "password": "string123",
  "lastName": "string123",
  "firstName": "string123",
  "middleName": "string123"
}

create_response = httpx.post("http://localhost:8000/api/v1/users", json = create_user_payload)
print(create_response.json())
print(create_response.status_code)