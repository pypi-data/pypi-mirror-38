import logging
from urllib.parse import urlparse

from flask import request
from flask.views import MethodView
from werkzeug.exceptions import MethodNotAllowed, NotFound
from werkzeug.routing import Map, Rule

logger = logging.getLogger(__name__)


class EndPointBase(MethodView):
    protected = True
    protected_endpoints = []

    base_url = None
    route = ""

    decorators = []

    def options(self, request, *args, **kwargs):
        return {"status": "ok"}

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        if meth is None:
            raise MethodNotAllowed(
                description={
                    "title": "Method is not allowed",
                    "detail": "Only following methods are allowed: {}.".format(
                        ", ".join(list(self.methods))
                    ),
                }
            )

        if not args and kwargs.get("request") is None:
            kwargs.update({"request": request})

        if self.route and self.base_url not in request.url:
            server_name = urlparse(request.url_root).netloc
            rule = Rule(self.route)
            url_map = Map([rule], strict_slashes=False)
            matcher = url_map.bind(server_name)
            try:
                matched_data = matcher.match(request.path)
            except NotFound:
                raise NotFound(
                    description={
                        "title": (
                            "The requested URL was not found on the server"
                        ),
                        "detail": (
                            "If you entered the URL manually please check your \
                            spelling and try again."
                        ),
                    }
                )
            endpoint_arguments = matched_data[1]
            kwargs.update(endpoint_arguments)

        return meth(*args, **kwargs)
