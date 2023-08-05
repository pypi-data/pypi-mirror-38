from bluemax import context
import time
import asyncio
from tornado import gen


__all__ = ["add", "a_add", "t_add"]


def add(a=2, b=2, sleep_for=0.1):
    """ returns a plus b syncronous."""
    result = a+b
    time.sleep(sleep_for)
    context.broadcast_on_success("action", {
        "name": "add",
        "result": result,
        "user": context.get_current_user() })
    return "add", result


async def a_add(a=2, b=3, sleep_for=0.2):
    """ returns a plus b, async native."""
    result = a+b
    await asyncio.sleep(sleep_for)
    context.broadcast_on_success("action", {
        "name": "a_add",
        "result": result,
        "user": context.get_current_user() })
    return "a_add", result


@gen.coroutine
def t_add(a=2, b=4, sleep_for=0.3):
    """ returns a plus b, async tornado."""
    result = a+b
    yield gen.sleep(sleep_for)
    context.broadcast_on_success("action", {
        "name": "t_add",
        "result": result,
        "user": context.get_current_user() })
    return "t_add", result
