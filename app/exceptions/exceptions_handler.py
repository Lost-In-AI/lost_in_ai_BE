from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI):
    async def unhandled_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "response_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error"}
        )

    async def validation_exception_handler(request: Request, exception: RequestValidationError):
        errors = exception.errors()
        message = "; ".join([f"{e['loc'][-1]}: {e['msg']}" for e in errors])
        return JSONResponse(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            content = {
                "response_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": f"VALIDATION ERROR: {message}"
            }
        )

    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
