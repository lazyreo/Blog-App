
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class Username(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20
    )

class UserCreate(Username):

    email: EmailStr

    password: str


class UserResponse(Username):
    id: int

    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreateResponse(BaseModel):
    status: str

    user: UserResponse

    model_config = ConfigDict(
        from_attributes=True
    )
