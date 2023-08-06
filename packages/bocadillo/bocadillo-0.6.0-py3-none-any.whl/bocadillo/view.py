import asyncio
import inspect
from typing import Callable, Union, Coroutine

from .compat import call_async
from .constants import ALL_HTTP_METHODS
from .request import Request
from .response import Response


class ClassBasedView:
    """Class-based view interface."""

    def get(self, request: Request, response: Response, **kwargs):
        raise NotImplementedError

    def post(self, request: Request, response: Response, **kwargs):
        raise NotImplementedError

    def put(self, request: Request, response: Response, **kwargs):
        raise NotImplementedError

    def patch(self, request: Request, response: Response, **kwargs):
        raise NotImplementedError

    def delete(self, request: Request, response: Response, **kwargs):
        raise NotImplementedError


# Types
CallableView = Callable[[Request, Response, dict], Coroutine]
View = Union[CallableView, ClassBasedView]


def create_callable_view(view: View) -> CallableView:
    """Create callable view from function (sync/async) or class based view."""
    if asyncio.iscoroutinefunction(view):
        return view
    elif inspect.isfunction(view):
        async def callable_view(req, res, **kwargs):
            await call_async(view, req, res, sync=True, **kwargs)

        return callable_view
    else:
        return _from_class_instance(view)


def _from_class_instance(view: ClassBasedView):
    def _find_for_method(method: str):
        try:
            return getattr(view, 'handle')
        except AttributeError:
            return getattr(view, method.lower())

    async def callable_view(req, res, **kwargs):
        view_ = _find_for_method(req.method)
        await call_async(view_, req, res, **kwargs)

    return callable_view


def get_view_name(view: View, base: ClassBasedView = None) -> str:
    def _get_name(obj):
        return getattr(obj, '__name__', obj.__class__.__name__)

    return '.'.join(_get_name(part) for part in (base, view) if part)


def get_declared_method_views(view: ClassBasedView):
    for method in ('handle', *map(str.lower, ALL_HTTP_METHODS)):
        if hasattr(view, method):
            yield method, getattr(view, method)
