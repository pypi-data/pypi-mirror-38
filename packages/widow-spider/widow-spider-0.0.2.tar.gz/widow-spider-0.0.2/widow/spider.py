#!/usr/bin/env python
"""
 Created by Dai at 18-11-6.
"""

import asyncio
import concurrent.futures
from multiprocessing import cpu_count

from widow.comsumer import start_comsumer
from widow.logger import get_logger
from widow.mid import Middleware
from widow.producer import start_producer
from widow.tasks import Meta

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider(metaclass=Meta):
    name = 'Python'
    logger = get_logger(__name__)

    request_config = {
        'sem': 3,
        'delay': 1,
        "timeout": 3
    }

    @classmethod
    async def start(cls):
        loop = asyncio.get_running_loop()

        for i in cls._fields:
            kwargs = cls._fields[i].kwargs
            res_list = [{
                'topic': i,
                'url': url,
                'kwargs': kwargs
            } for url in cls._fields[i].url]
            for res in res_list:
                Middleware.requests_queue.put(res)

        # 3. Run in a custom process pool:
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count() - 1) as pool:

            asyncio.ensure_future(loop.run_in_executor(
                pool, start_producer, cls.request_config
            ))
            for i in range(1, cpu_count()):
                asyncio.ensure_future(loop.run_in_executor(
                    pool, start_comsumer, cls._fields))
