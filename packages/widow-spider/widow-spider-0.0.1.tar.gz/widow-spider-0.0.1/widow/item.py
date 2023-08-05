#!/usr/bin/env python
"""
 Created by Dai at 18-11-8.
"""

from inspect import iscoroutinefunction

from lxml import etree

from widow.field import BaseField


class ItemMeta(type):
    """
    Metaclass for an item
    """

    def __new__(cls, name, bases, attrs):
        __fields = dict({(field_name, attrs.pop(field_name)) for field_name, object in list(attrs.items()) if
                         isinstance(object, BaseField)})
        attrs['__fields'] = __fields
        new_class = type.__new__(cls, name, bases, attrs)
        return new_class


class Item(metaclass=ItemMeta):
    """
    Item class for each item
    """

    def __init__(self):
        self.results = {}

    @classmethod
    async def get_item(cls, content: bytes = b'', tree: etree._Element = None, **kwargs) -> object:
        if tree is None:
            tree = etree.HTML(content)
        return await cls._parse_html(tree)

    @classmethod
    async def get_items(cls, content=b'', tree: etree._Element = None, **kwargs) -> list:
        """
        :param content:
        :param tree:
        :param kwargs:
        :return:
        """
        if tree:
            etree_result = etree
        else:
            etree_result = etree.HTML(content)
        items_field = getattr(cls, '__fields', {}).get('target_item', None)
        if items_field:
            items = items_field.extract_value(etree_result, is_source=True)
            if items:
                tasks = [cls._parse_html(etree_result=i) for i in items]
                all_items = []
                for task in tasks:
                    all_items.append(await task)
                return all_items
            else:
                raise ValueError("Get target_item's value error!")
        else:
            raise ValueError("target_item is expected")

    @classmethod
    async def _parse_html(cls, etree_result: etree._Element) -> object:
        """
        根据所给的etree 返回对应内容
        :param etree_result:
        :return:
        """
        if etree_result is None or not isinstance(etree_result, etree._Element):
            raise ValueError("etree._Element is expected")
        item_ins = cls()
        for field_name, field_value in getattr(item_ins, '__fields', {}).items():
            if not field_name.startswith('target_'):
                clean_method = getattr(item_ins, 'clean_%s' % field_name, None)
                value = field_value.extract_value(etree_result) if isinstance(field_value, BaseField) else field_value
                if clean_method is not None:
                    if iscoroutinefunction(clean_method):
                        value = await clean_method(value)
                    else:
                        value = clean_method(value)
                setattr(item_ins, field_name, value)
                item_ins.results[field_name] = value
        return item_ins

    def __str__(self):
        return f"<Item {self.results}>"
