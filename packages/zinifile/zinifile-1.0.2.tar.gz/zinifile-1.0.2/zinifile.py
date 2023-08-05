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

import configparser


class _node():
    def __init__(self, data):
        self._base = data
        self._next_index = 0
        self._items = {key: self._build_node(self._base[key]) for key in self._base}
        self._iter_items = [(key, value) for key, value in self._items.items()]

    def items(self):
        return self._iter_items

    def get(self, key):
        return self._items.get(key)

    def _build_node(self, data):
        if isinstance(data, str):
            return data
        return _node(data)

    def __getattr__(self, key):
        return self._items.get(key)

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_index >= len(self._items):
            self._next_index = 0
            raise StopIteration

        key = self._iter_items[self._next_index][0]
        self._next_index += 1
        return key


def load(file_name, encoding='utf8'):
    config = configparser.ConfigParser()
    config.read(file_name, encoding=encoding)
    return _node(config)


def load_text(text):
    config = configparser.ConfigParser()
    config.read_string(text)
    return _node(config)
