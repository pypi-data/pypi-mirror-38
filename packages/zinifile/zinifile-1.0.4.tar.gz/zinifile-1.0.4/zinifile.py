# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zinifile.py
   Author :       Zhang Fan
   date：         2018/10/14
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import re
import configparser

_is_int_re = re.compile('^[-+]?\d+$')
_is_float_re = re.compile('^[-+]?\d+\.\d+$')


class _node():
    def __init__(self, data):
        self._base = data
        self._next_index = 0
        self._items = {key: self.__build_node(value) for key, value in self._base.items()}
        self._iter_items = [(key, value) for key, value in self._items.items()]

    def items(self):
        return self._iter_items

    def get(self, key, default=None):
        return self._items.get(key, default)

    def __build_node(self, data):
        if isinstance(data, str):
            return self.__parser_config_value(data)
        return _node(data)

    def __parser_config_value(self, value):
        if not value:
            return None

        elif 'true' == value.lower():
            return True
        elif 'false' == value.lower():
            return False

        return self.__str_to_num(value, value)

    def __getattr__(self, key):
        if key in self._items:
            return self._items[key]
        return empty_node

    def __getitem__(self, key):
        return self._items[key]

    def __contains__(self, key):
        return key in self._items

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_index >= len(self._items):
            self._next_index = 0
            raise StopIteration

        key = self._iter_items[self._next_index][0]
        self._next_index += 1
        return key

    def __str_to_num(self, text, default=None):
        try:
            return int(_is_int_re.search(text).group())
        except:
            pass

        try:
            return float(_is_float_re.search(text).group())
        except:
            return default


class empty_node(_node):
    def __init__(self):
        super().__init__(dict())

    def __bool__(self):
        return False

    def __eq__(self, other):
        return other is None

empty_node = empty_node()


def load(file_name, encoding='utf8'):
    config = configparser.ConfigParser()
    config.read(file_name, encoding=encoding)
    return _node(config)


def load_text(text):
    config = configparser.ConfigParser()
    config.read_string(text)
    return _node(config)


if __name__ == '__main__':
    print(empty_node is None)
    print(empty_node == None)
    print(bool(empty_node))
