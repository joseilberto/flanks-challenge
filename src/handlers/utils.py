"""Util methods"""

from typing import Callable, no_type_check

from sanic.request import Request
from sanic.response import JSONResponse, json


@no_type_check
def async_request_params(fun: Callable):
    """Decorator method to collect the parameters of a request"""

    @no_type_check
    async def wrapper(cls: object, request: Request) -> JSONResponse:
        """Wrapper to call the fun method using the request parameters"""
        return json(await fun(cls, **request.json))

    return wrapper
