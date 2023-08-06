from functools import WRAPPER_ASSIGNMENTS, wraps

from .utils import trailing_slash


def patched_wraps(func):
    assigned = WRAPPER_ASSIGNMENTS + (
        "view_class",
        "methods",
        "provide_automatic_options",
    )
    return wraps(func, assigned=assigned)


def configure_routes(app, handlers):
    for handler in handlers:
        app.add_url_rule(
            trailing_slash(
                handler.view_class.base_url + handler.view_class.route
            ),
            view_func=handler,
        )
