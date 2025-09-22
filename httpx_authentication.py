import httpx

payload_login = {
  "email": "userAV@example.com",
  "password": "1478965"
}

response_login = httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload_login)
response_login_data = response_login.json()

print("Login response:", response_login_data)
print("Status Code:", response_login.status_code)

payload_refresh =  {
  "refreshToken": response_login_data['token']['refreshToken']
}
response_refresh = httpx.post("http://localhost:8000/api/v1/authentication/refresh", json=payload_refresh)
response_refresh_data = response_login.json()
print("Refresh response:", response_refresh)
print("Status Code:", response_refresh.status_code)


client = httpx.Client(headers = {"Authorization" : f"Bearer {response_login_data['token']['accessToken']}"})
response_me = client.get("http://localhost:8000/api/v1/users/me")
print("Me response:", response_me.json())
print("Me Code:", response_me.status_code)