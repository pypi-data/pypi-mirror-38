import functools
import re
from inspect import signature
from . import ErrorHandler, FailureReason
from ..exceptions import DecorationError


class AioHttpProvider:
    def __init__(self, db_provider, error_handler=ErrorHandler.PASS_AS_VARIABLE):
        self.db_provider = db_provider
        self.error_handler = error_handler

    async def _fail(self, func, request, failure_reason):
        if self.error_handler is ErrorHandler.PASS_AS_VARIABLE:
            return await func(request, failure_reason)

    def _resolve_params_map(self, search):
        m = re.findall("\{(.*?)\}", search)
        params = {}
        for match in m:
            k, v = tuple(match.split(":"))
            params[k] = v
        return params

    def _get_params(self, params, req):
        ret_params = {}
        for param, location in params:
            if location == 'match':
                ret_params[param] = req.match_info[param]
            elif location == 'query':
                ret_params[param] = req.query[param]
            elif location == 'reqvar':
                ret_params[param] = req[param]
        return ret_params

    def requires_permission(self, permission):
        def decorator(func):
            if self.error_handler is ErrorHandler.PASS_AS_VARIABLE:
                sig = signature(func, follow_wrapped=False)
                if "abac_error" not in sig.parameters:
                    raise DecorationError(
                        func,
                        f"{func.__module__ }.{func.__qualname__}",
                        "Told to pass error as variable,"
                        + " but there was no abac_error parameter",
                    )
            params = self._resolve_params_map(permission)

            @functools.wraps(func)
            async def wrapper(request):
                if not request["user"]:
                    return await self._fail(func, request, FailureReason.NOT_LOGGED_IN)
                nonlocal params
                params_matches = self._get_params(self, params, request)

            return wrapper

        return decorator
    
    def requires_role(self, role):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(request):
                return await func(request)
