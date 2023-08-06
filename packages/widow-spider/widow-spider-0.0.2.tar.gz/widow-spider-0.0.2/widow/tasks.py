#!/usr/bin/env python
"""
 Created by Dai at 18-11-7.
"""

from widow.logger import get_logger

from widow.mid import Middleware


class BaseTask:
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.logger = get_logger(__name__)

    async def start(self, res):
        await self.parse(res)
        Middleware.tasks_queue.get_nowait()

    async def parse(self, res):
        self.logger.info(res)

    async def requests(self, topic, url, **kwargs):
        res = {
            "topic": topic,
            "url": url,
            "kwargs": kwargs
        }
        Middleware.requests_queue.put(res)


class Meta(type):
    # 把自动构建的类同一放入_fields
    def __new__(cls, name, bases, attrs):
        _fields = dict({(field_name, attrs.pop(field_name)) for field_name, object in list(attrs.items()) if
                        isinstance(object, BaseTask)})  ##
        attrs['_fields'] = _fields

        new_class = super(Meta, cls).__new__(cls, name, bases, attrs)
        return new_class


if __name__ == '__main__':
    pass
