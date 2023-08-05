#!/usr/bin/env python
"""
 Created by Dai at 18-11-7.
"""

import asyncio

from widow.logger import get_logger
from widow.mid import Middleware

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


def start_comsumer(field):
    try:
        Comsumer(field=field)
    except:
        return


class Comsumer:

    def __init__(self, field):

        self.field = field
        self.logger = get_logger(__name__)
        asyncio.run(self.start())

    async def start(self):
        while True:
            try:
                res = Middleware.rensponce_queue.get_nowait()
                asyncio.ensure_future(self.field[res['topic']].start(res))
            except Exception as e:
                await asyncio.sleep(1)
                if Middleware.judge():
                    self.logger.info(f"finish")
                    tasks = [task for task in asyncio.Task.all_tasks() if task is not
                             asyncio.tasks.Task.current_task()]
                    list(map(lambda task: task.cancel(), tasks))
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    asyncio.get_running_loop().stop()
