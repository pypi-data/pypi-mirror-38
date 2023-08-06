# -*- coding: utf-8 -*-

import codecs
import encodings
import io
import sys

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


class StreamReader(utf_8.streamreader):

    _stream = None
    _decoded = False

    # decode is deferred to support better error messages

    @property
    def stream(self):
        if not self._decoded:
            text, _ = decode(self._stream.read())
            self._stream = io.BytesIO(text.encode('utf-8'))
            self._decoded = True
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream
        self._decoded = False


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):

    def _buffer_decode(self, input, errors, final):
        if final:
            return decode(input, errors)
        return '', 0


try:
    eval("f'Hello world.'")
except SyntaxError:
    decode = utf_8.decode
    StreamReader = utf_8.streamreader
    IncrementalDecoder = utf_8.incrementaldecoder


codec_map = {
    name: codecs.CodecInfo(
        name=name,
        encode=utf_8.encode,
        decode=decode,
        incrementalencoder=utf_8.incrementalencoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=utf_8.streamwriter,
        streamreader=StreamReader,
    )
    for name in ('f2format', 'f2format-codec', 'f2format_codec')
}


def register():
    codecs.register(codec_map.get)


if __name__ == '__main__':
    sys.exit(f2format.main())
