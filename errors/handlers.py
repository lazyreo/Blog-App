from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from errors import exceptions


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(exceptions.BlogIDNotFoundException)
    async def blog_not_found_handler(
        request: Request,
        exc: exceptions.BlogIDNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "code": "BLOG_ID_NOT_FOUND",
                    "message": f"Blog with ID {exc.blog_id} was not found."
                }
            }
        )

    @app.exception_handler(exceptions.EmailAlreadyExistsException)
    async def email_already_exists_handler(
        request: Request,
        exc: exceptions.EmailAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": f"{exc.email} already exists. Do you wish to login?"
                }
            }
        )

    @app.exception_handler(exceptions.UsernameAlreadyTakenException)
    async def username_already_taken_handler(
        request: Request,
        exc: exceptions.UsernameAlreadyTakenException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error": {
                    "code": "USERNAME_ALREADY_TAKEN",
                    "message": f"{exc.username} already taken"
                }
            }
        )

    @app.exception_handler(exceptions.UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: exceptions.UserNotFoundException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": {
                    "code": "USER_NOT_FOUND",
                    "user": exc.user or None
                }
            }
        )

    @app.exception_handler(exceptions.InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: exceptions.InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Incorrect username or password"
                }
            }
        )

    @app.exception_handler(exceptions.InvalidTokenException)
    async def invalid_token_handler(
        request: Request,
        exc: exceptions.InvalidTokenException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Invalid token"
                }
            }
        )
