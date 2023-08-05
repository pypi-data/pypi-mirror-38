#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import functools

import joker.textmanip
from joker.cast import cache_lookup
from joker.cast.iterative import nonblank_lines_of
from joker.place import under_package_dir

_cache = {}


def const(func):
    return functools.wraps(func)(lambda: cache_lookup(_cache, func, func))


def const1(func):
    return functools.wraps(func)(
        lambda k: cache_lookup(_cache, (func, k), func, k)
    )


@const
def get_unicode_blocks():
    path = under_package_dir(joker.textmanip, 'asset/unicode_blocks.txt')
    results = []
    for head, tail, title in nonblank_lines_of(path):
        head = int(head, base=0)
        tail = int(tail, base=0)
        results.append((head, tail, title))


def search_unicode_blocks(pattern):
    import re
    regex = re.compile(pattern)
    blocks = []
    for tup in get_unicode_blocks:
        if regex.search(tup[2]):
            blocks.append(tup)
    return blocks


def blocks_to_name_tuple_map(blocks=None):
    if blocks is None:
        blocks = get_unicode_blocks()
    return {tu[2]: tuple(tu[:2]) for tu in blocks}


@const
def get_all_encodings():
    path = under_package_dir(joker.textmanip, 'asset/encodings.txt')
    return list(nonblank_lines_of(path))


@const1
def get_most_frequent_characters(lang='sc'):
    path = 'dataset/mfc-{}.txt'.format(lang)
    path = under_package_dir(joker.textmanip, path)
    return ''.join(nonblank_lines_of(path))
