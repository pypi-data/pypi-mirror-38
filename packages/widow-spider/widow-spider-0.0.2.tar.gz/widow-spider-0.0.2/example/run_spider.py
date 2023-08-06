#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18-11-10 上午9:03
@author: dai
"""

import asyncio

from example.spider_bd_tieba import BDTiebaItemTask, BDTiebaPageItemTask, BDtiebaDetailItemsTask
from example.spider_stock_id import StockIdTask
from widow.spider import Spider


class mainSpider(Spider):
    stock_id = StockIdTask(url=['http://quote.eastmoney.com/stocklist.html#sz'])

    bd_t2 = BDTiebaPageItemTask(url=[])

    bd_t1 = BDTiebaItemTask(url=[f"https://tieba.baidu.com/f?kw=德云色&ie=utf-8&pn={str(i*50)}" for i in range(0, 10)])

    bd_t3 = BDtiebaDetailItemsTask(url=[])


asyncio.run(mainSpider.start())
