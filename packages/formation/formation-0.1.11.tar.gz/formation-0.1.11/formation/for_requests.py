import requests
from .formation import wrap

__all__ = ["build_sender"]


def build_sender(middleware=[]):
    wrapped = wrap(requests_adapter, middleware=middleware)

    def sender(method, url, **kwargs):
        ctx = {"req": {"method": method, "url": url}}
        ctx["req"].update(kwargs)
        ctx = wrapped(ctx)
        return ctx["res"]

    return sender


def requests_adapter(ctx):
    req = ctx["req"]
    meth = getattr(requests, req.get("method", "get").lower())
    # TODO ship var as kwargs and not explicitly
    res = meth(
        req["url"],
        headers=req.get("headers", {}),
        params=req.get("params", {}),
        auth=req.get("auth", None),
        data=req.get("data", None),
    )
    ctx["res"] = res
    return ctx
