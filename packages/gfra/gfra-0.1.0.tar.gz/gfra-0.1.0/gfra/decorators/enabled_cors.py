from flask import make_response

from ..helpers import patched_wraps


def enabled_cors(
    allowed_headers=[
        "Origin",
        "X-Requested-With",
        "Content-Type",
        "Acccept",
        "Authorization",
    ],
    allowed_origin="*",
    allowed_methods=["GET", "POST", "HEAD", "DELETE", "OPTIONS"],
):
    allowed_headers_string = ", ".join(allowed_headers)
    allowed_methods_string = ",".join(allowed_methods)

    def decorator(func):
        @patched_wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            response = make_response(result)
            response.headers[
                "Access-Control-Allow-Headers"
            ] = allowed_headers_string
            response.headers["Access-Control-Allow-Origin"] = allowed_origin
            response.headers[
                "Access-Control-Allow-Methods"
            ] = allowed_methods_string
            return response

        return wrapper

    return decorator
