import functools
import re
from inspect import signature
from . import ErrorHandler, FailureReason
from ..exceptions import DecorationError


class AioHttpProvider:
    def __init__(
        self, db_provider, error_handler=ErrorHandler.PASS_AS_VARIABLE, active=True
    ):
        self.db_provider = db_provider
        self.error_handler = error_handler
        self.active = active

    async def _fail(self, func, request, failure_reason):
        if self.error_handler is ErrorHandler.PASS_AS_VARIABLE:
            return await func(request, failure_reason)

    async def _ok(self, func, request):
        if self.error_handler is ErrorHandler.PASS_AS_VARIABLE:
            return await func(request, None)
        return await func(request)

    def _resolve_params(self, search):
        m = re.findall(r"\{(.*?)\}", search)
        params = []
        for match in m:
            params.append(match)
        return params

    def _get_params(self, params, req):
        ret_params = {}
        for param in params:
            if param in req:
                ret_params[param] = req[param]
            elif param in req.match_info:
                ret_params[param] = req.match_info[param]
            elif param in req.query:
                ret_params[param] = req.query[param]
        # for param, location in params:
        #     if location == 'match':
        #         ret_params[param] = req.match_info[param]
        #     elif location == 'query':
        #         ret_params[param] = req.query[param]
        #     elif location == 'reqvar':
        #         ret_params[param] = req[param]
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
            params = self._resolve_params(permission)

            @functools.wraps(func)
            async def wrapper(request):
                if not self.active:
                    return await self._ok(func, request)
                if not request["user"]:
                    return await self._fail(func, request, FailureReason.NOT_LOGGED_IN)
                nonlocal params
                params_matches = self._get_params(self, params, request)
                final_perm = permission.format_map(params_matches)
                if not self.db_provider.user_has_permission(
                    request["user_id"], final_perm
                ):
                    return await self._fail(
                        func, request, FailureReason.MISSING_PERMISSION
                    )
                return await self._ok(func, request)

            return wrapper

        return decorator

    def requires_role(self, role):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(request):
                if not self.active:
                    return self._ok(func, request)
                return await self._ok(func, request)
