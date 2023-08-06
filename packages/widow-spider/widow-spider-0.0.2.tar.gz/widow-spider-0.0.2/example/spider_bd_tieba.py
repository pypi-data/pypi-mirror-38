#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18-11-10 上午9:01
@author: dai
"""

from example.tools import code_format, Time

from widow.field import TextField, AttrField
from widow.item import Item
from widow.tasks import BaseTask


class BDTiebaItem(Item):
    """
        获取贴吧内的帖子标题
    """
    spider_name = 'baidu_tieba'

    target_item = TextField(css_select='li>div.t_con')

    title_text = AttrField(css_select='a.j_th_tit', attr='title')
    url = AttrField(css_select='a.j_th_tit', attr='href')
    nickname = TextField(css_select='span.frs-author-name-wrap')

    async def clean_title_text(self, title_text):
        if isinstance(title_text, str):
            return title_text.replace('\u200e', '')
        else:
            return None

    async def clean_url(self, url):
        if isinstance(url, str):
            return 'https://tieba.baidu.com' + url
        else:
            return None


class BDTiebaGetPageItem(Item):
    """
        获取该贴有多少页
    """

    page_num = TextField(css_select='li.l_reply_num span.red:nth-of-type(2)')

    async def clean_page_num(self, page_num):
        if isinstance(page_num, str):
            return page_num
        else:
            for i in page_num:
                return ''.join(i.text.strip().replace('\xa0', ''))


class BDTiebaDetailsItem(Item):
    """
        获取楼主所发的内容
    """
    target_item = TextField(css_select='div.l_post')

    lz_text = TextField(css_select='div.d_post_content')
    post_time = TextField(css_select='span.tail-info:nth-of-type(4)')
    lz_name = TextField(css_select='li.d_name')

    async def clean_lz_text(self, lz_text):
        if isinstance(lz_text, str):
            return lz_text
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in lz_text])

    async def clean_post_time(self, post_time):
        if isinstance(post_time, str):
            return post_time
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in post_time])


class BDTiebaItemTask(BaseTask):

    async def parse(self, res):
        """
            在需要复用etree时 直接传入 etree
        :param res:
        :return:
        """
        try:
            items = await BDTiebaItem.get_items(content=res['data'])
            for item in items:
                if item.url:
                    res = {
                        "post_url": item.url,
                        "post_lz_name": item.nickname,
                        "post_title": item.title_text
                    }
                    #  print(res)
                    await self.requests(topic='bd_t2', url=item.url)

        except Exception as e:
            self.logger.error(e)


class BDTiebaPageItemTask(BaseTask):

    async def parse(self, res):
        """
            在需要复用etree时 直接传入 etree
        :param res:
        :return:
        """

        try:
            item = await BDTiebaGetPageItem.get_item(content=res['data'])
            page_num = item.page_num
            for i in range(1, int(page_num)):
                url = str(res['url']) + '?pn=' + str(int(i) + 1)
                await self.requests(topic='bd_t3', url=url)

        except Exception as e:
            self.logger.error(e)


class BDtiebaDetailItemsTask(BaseTask):

    async def parse(self, res):
        details_list = []
        try:
            datas = await BDTiebaDetailsItem.get_items(content=res['data'])
            for data in datas:
                if (data.lz_text):
                    temp = {
                        'post_url': res['url'][:res['url'].index('?')],
                        'post_content': code_format(data.lz_text),
                        'post_time': Time(f"{data.post_time}:00").datetime if data.post_time else data.post_time,
                        "post_name": code_format(data.lz_name)
                    }
                    details_list.append(temp)

        except Exception as e:
            self.logger.error(e)
        # print(details_list)
