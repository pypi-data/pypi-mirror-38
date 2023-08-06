#!/usr/bin/env python
# encoding: utf-8

__all__ = ["version", "version_info"]

from .version import version, version_info


def register():
    codec_name = "ibm935"
    try:
        "".encode(codec_name)
    except LookupError:
        pass
    else:
        return

    import sys
    import os
    import struct
    import codecs

    if sys.version_info > (3,):
        _chr = chr
    else:
        _chr = unichr

    U2C = {}
    C2U = {}

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "data"), "rb") as f:
        while True:
            block = f.read(4)
            if not block:
                break
            _u, _c = struct.unpack(">H2s", block)
            _u = _chr(_u)
            if _c[:1] == b'\x00':
                _c = _c[1:]
            U2C[_u] = _c
            C2U[_c] = _u

    def ibm935_encode(src, errors='strict'):
        word_flag = False
        buf = []
        for idx in range(len(src)):
            u = src[idx]
            c = U2C.get(u, b'\x6f')
            if not word_flag and len(c) > 1:
                buf.append(b'\x0e')
                word_flag = True
            elif word_flag and len(c) == 1:
                buf.append(b'\x0f')
                word_flag = False
            buf.append(c)

        if word_flag:
            buf.append(b'\x0f')

        return b''.join(buf), len(src)

    def ibm935_decode(src, errors='strict'):
        read_length = 1
        buf = []
        idx = 0
        while idx < len(src):
            if src[idx] == b'\x0e'[0]:
                read_length = 2
                idx += 1
                continue

            if src[idx] == b'\x0f'[0]:
                read_length = 1
                idx += 1
                continue

            c = src[idx: idx + read_length]
            if len(c) < read_length:
                # source bytes were truncated
                break

            u = C2U.get(c, '?')
            buf.append(u)
            idx += read_length

        return ''.join(buf), len(src)

    class Codec(codecs.Codec):
        def encode(self, src, errors='strict'):
            return ibm935_encode(src, errors)

        def decode(self, src, errors='strict'):
            return ibm935_decode(src, errors)

    # todo(Eric Wong): to handle discrete double-bytes
    class IncrementalEncoder(codecs.IncrementalEncoder):
        def encode(self, src, final=False):
            return ibm935_encode(src, self.errors)[0]

    # todo(Eric Wong): to handle discrete double-bytes
    class IncrementalDecoder(codecs.IncrementalDecoder):
        def decode(self, src, final=False):
            return ibm935_decode(src, self.errors)[0]

    class StreamWriter(Codec, codecs.StreamWriter):
        pass

    class StreamReader(Codec, codecs.StreamReader):
        pass

    def search_func(name):
        if name == codec_name:
            return codecs.CodecInfo(
                name=codec_name,
                encode=ibm935_encode,
                decode=ibm935_decode,
                incrementalencoder=IncrementalEncoder,
                incrementaldecoder=IncrementalDecoder,
                streamwriter=StreamWriter,
                streamreader=StreamReader,
            )

    codecs.register(search_func)


register()
