#!/usr/bin/env python
"""
 Created by Dai at 18-11-7.
"""

import asyncio

import pyppeteer

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
import async_timeout

from widow.logger import get_logger
from widow.mid import Middleware

import aiohttp
import os

os.environ['PYPPETEER_CHROMIUM_REVISION'] = '575458'
"""
    第一次加载现在 CHROMIUM 需要自备梯子
    若显示无法找到 浏览器 查看自己下载的 浏览器版本
    ubuntu 下报错 无法找到 nss_3.22 直接装一个Google 解决
    或者 https://pkgs.org/download/libnss3
    
"""


def start_producer(config):
    try:
        Producer(config)
    except:
        return


class Producer:

    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        asyncio.run(self.start())

    async def start(self):
        self.sem = asyncio.Semaphore(self.config.get('sem', 3))

        while True:
            try:
                res = Middleware.requests_queue.get_nowait()
                Middleware.tasks_queue.put('')
                asyncio.ensure_future(self.request(res=res))
            except Exception as e:
                await asyncio.sleep(1)
                if Middleware.judge():
                    self.logger.info(f"finish")
                    if hasattr(self, "browser"):
                        await self.browser.close()
                    tasks = [task for task in asyncio.Task.all_tasks() if task is not
                             asyncio.tasks.Task.current_task()]
                    list(map(lambda task: task.cancel(), tasks))
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    asyncio.get_running_loop().stop()

                    while True:
                        try:
                            res = Middleware.faild_queue.get(timeout=0)
                            self.logger.info(f"失败消息 ： {res} ")
                        except Exception as e:
                            break

    async def request(self, res):
        self.logger.info(res)

        for i in range(3):
            try:
                async with self.sem:
                    if self.config.get('delay', 0):
                        await asyncio.sleep(self.config.get('delay'))
                    async with async_timeout.timeout(self.config.get('timeout', 3)):
                        if res['kwargs'].get('load_js', False):
                            if not hasattr(self, "browser"):
                                self.browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
                            page = await  self.browser.newPage()
                            res = await page.goto(res['url'], options={'timeout': int(3 * 1000)})
                            data = await page.content()
                            Middleware.rensponce_queue.put({'data': data, **res})
                        else:
                            async with aiohttp.ClientSession() as sess:
                                async with sess.get(url=res['url'], **res['kwargs']) as resp:
                                    res_status = resp.status
                                    assert res_status in [200, 201]
                                    data = await resp.read()
                                    Middleware.rensponce_queue.put({'data': data, **res})
                    return
            except Exception as e:
                self.logger.error(f"请求失败，参数{res} error : {e} retry:{i}")

        Middleware.tasks_queue.get()
        Middleware.faild_queue.put(res)
