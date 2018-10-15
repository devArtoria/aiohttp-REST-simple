import inspect
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web import Request, Response
from multidict import CIMultiDict


class EndpointBase:

    def __init__(self, allowed_methods: set=('GET', 'POST', 'PUT',
                                             'DELETE', 'PATCH', 'HEAD',
                                             'OPTIONS', 'TRACE', 'CONNECT')):
        self.allowed_methods = allowed_methods
        self.methods = {}

        for method_name in allowed_methods:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name: str, method):
        self.methods[method_name.upper()] = method

    async def options(self, request: Request):
        return Response(headers=CIMultiDict(
            Allow=" ".join(self.allowed_methods)))

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())

        if not method:
            raise HTTPMethodNotAllowed('', self.allowed_methods)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})
        unsatisfied_args = set(wanted_args) - set(available_args.keys())

        if unsatisfied_args:
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name]
                            for arg_name in wanted_args})
