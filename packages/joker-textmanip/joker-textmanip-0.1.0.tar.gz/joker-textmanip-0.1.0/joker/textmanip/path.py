#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import re
import datetime


def url_to_filename(url):
    # http://stackoverflow.com/questions/295135/
    name = re.sub(r'[^\w\s_.-]+', '-', url)
    return re.sub(r'^{http|https|ftp}', '', name)


def ext_join(path, ext):
    """
    >>> ext_join('~/html/index.txt', 'html')
    '~/html/index.html'
    >>> ext_join('~/html/index.txt', '.html')
    '~/html/index.txt.html'

    :param path: (str)
    :param ext: (str)
    :return:
    """
    if ext.startswith(os.path.extsep):
        return path + ext
    p, _ = os.path.splitext(path)
    return p + os.path.extsep + ext


smart_extension_join = ext_join


def unix_filename_safe(s):
    # ASCII 47: "/"
    return s.translate(dict.fromkeys([0, 47]))


windows_reserved_names = {
    'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
    'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
    'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
}


def windows_filename_safe(s):
    # <>:"/\\|?* and ASCII 0 - 31
    # https://stackoverflow.com/a/31976060/2925169
    ordinals = [ord(c) for c in '<>:"/\\|?*']
    ordinals.extend(range(32))
    s = s.translate(dict.fromkeys(ordinals))
    if s.endswith(' ') or s.endswith('.'):
        s = s[:-1]
    if s.upper() in windows_reserved_names:
        s += '_'
    return s


def proper_filename(s):
    s = windows_filename_safe(s.strip())
    # remove leading .-, and repl quotes/spaces with _
    s = re.sub(r'^[.-]', '', s)
    s = re.sub(r"['\s]+", '_', s)
    s = re.sub(r'\s*\(([0-9]+)\)\.', r'-\1.', s)
    return s


def adapt_outpath(path, outpath, ext):
    if outpath is None:
        outpath = os.path.splitext(path)[0] + ext
    while os.path.exists(outpath):
        stempath, ext = os.path.splitext(outpath)
        a = stempath, datetime.datetime.now(), id(stempath) % 100, ext
        outpath = '{}.{:%y%m%d-%H%M%S}-{:02}{}'.format(*a)
    return outpath


def check_outpath(path, outpath, ext):
    if outpath is None:
        outpath = os.path.splitext(path)[0] + ext
    if os.path.exists(outpath):
        raise FileExistsError(outpath)
    return outpath

