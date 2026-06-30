

from typing import Optional

from pydantic import EmailStr

from models.user_model import User


class BlogIDNotFoundException(Exception):
    def __init__(
        self,
        blog_id: int
    ):

        self.blog_id = blog_id


class UsernameAlreadyTakenException(Exception):
    def __init__(
        self,
        username: str
    ):

        self.username = username


class EmailAlreadyExistsException(Exception):
    def __init__(
        self,
        email: EmailStr
    ):

        self.email = email


class UserNotFoundException(Exception):
    def __init__(
        self,
        user: Optional[User]
    ):
        if user:
            self.user = user


class InvalidCredentialsException(Exception):
    def __init__(
        self
    ):
        pass


class InvalidTokenException(Exception):
    def __init__(
        self
    ):
        pass
