import argon2
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# Hash password


def hash_password(password: str) -> bytes:
    return argon2.hash_password(password.encode("utf-8"))

# Verify password


def verify_password(
    password_input: str,
    hashed_password: bytes
) -> bool:

    return argon2.verify_password(
        hashed_password,
        password_input.encode("utf-8")
    )
