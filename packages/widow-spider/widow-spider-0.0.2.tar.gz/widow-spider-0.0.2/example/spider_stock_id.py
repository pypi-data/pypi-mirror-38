#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18-11-10 上午9:00
@author: dai
"""

import asyncio

from widow.field import TextField, AttrField
from widow.item import Item
from widow.spider import Spider
from widow.tasks import BaseTask


class StockIdItem(Item):
    target_item = TextField(css_select='div.quotebody li')
    stock_url = AttrField(css_select='a', attr='href')
    stock_id = TextField(css_select='a')


class StockIdTask(BaseTask):

    @classmethod
    async def parse(cls, res):
        """
            在需要复用etree时 直接传入 etree
        :param res:
        :return:
        """

        items = await StockIdItem.get_items(content=res['data'])
        for item in items:
            print(item.stock_id)
            print(item.stock_url)


class StockSpider(Spider):
    stock_id = StockIdTask(url=['http://quote.eastmoney.com/stocklist.html#sz'])


if __name__ == '__main__':
    asyncio.run(StockSpider.start())
