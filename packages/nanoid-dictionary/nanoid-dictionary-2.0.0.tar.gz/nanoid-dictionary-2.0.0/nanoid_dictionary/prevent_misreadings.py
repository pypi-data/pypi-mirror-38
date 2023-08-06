# coding: utf-8

import re


def match_all_unsafe_symbols(symbols):
    return '[%s]' % symbols


def prevent_misreadings(string, unsafe_chars):
    return re.sub(match_all_unsafe_symbols(unsafe_chars), '', string, flags=re.IGNORECASE)
