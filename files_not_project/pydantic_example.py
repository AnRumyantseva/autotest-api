from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email:str
    address: Address
    is_active: bool = True


user = User(
    id=1,
    name="Alice",
    email="alice@example.com",
    address={"city": "New York", "zip_code": "10001"}
)
print(user.address, type(user.address))
print(user.model_dump())
print(user.model_dump_json())

class UserSecond(BaseModel):
    id: int
    name: str
    email:str
    is_active: bool = Field(alias="isActive")


user_data = {
    'id' : 1,
    'name' : "Alice",
    'email' : 'Alice@example.com',
    'isActive' : True
}

userSecond = UserSecond(**user_data)
print(userSecond)