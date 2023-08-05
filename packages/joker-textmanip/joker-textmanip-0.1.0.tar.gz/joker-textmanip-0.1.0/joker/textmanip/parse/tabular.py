#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from collections import OrderedDict

from joker.cast.iterative import nonblank_lines_of


def _split2(s):
    parts = s.strip().split(None, 1)
    while len(parts) < 2:
        parts.append(None)
    return tuple(parts)


def text_to_dict(lines, reverse=False):
    if isinstance(lines, str):
        lines = lines.splitlines()
    tups = [_split2(x) for x in lines]
    if reverse:
        tups = [tu[::-1] for tu in tups]
    # print('debug: tups', tups)
    return OrderedDict(tups)


# compat with previous version
two_columns_to_dict = text_to_dict


def textfile_to_dict(path, reverse=False):
    return text_to_dict(nonblank_lines_of(path), reverse=reverse)


def dataframe_to_dicts(df):
    """
    :param df: (pandas.DataFrame)
    :return: (list) a list of dicts, each for a row of the dataframe
    """
    return list(df.T.to_dict().values())
