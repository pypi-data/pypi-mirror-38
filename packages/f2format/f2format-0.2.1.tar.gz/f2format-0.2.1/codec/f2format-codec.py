# -*- coding: utf-8 -*-

import codecs
import encodings
import io

import f2format

# codecs.CodecInfo of UTF-8
utf_8 = encodings.search_function('utf-8')


def decode(byte, errors='strict'):
    string, length = utf_8.decode(byte, errors)

    lineno = {1: 0}     # line number -> file offset
    for lnum, line in enumerate(io.StringIO(string), start=1):
        lineno[lnum+1] = lineno[lnum] + len(line)
    text = f2format.convert(string, lineno)

    return text, length
