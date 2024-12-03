"""
decode.py

decode is a SCTE-35 decoder function
with input type auto-detection.

SCTE-35 data can be parsed with just
one function call.

the arg gonzo is the input.
if gonzo is not set, decode will attempt
to read mpegts video from sys.stdin.buffer.

SCTE-35 data is printed in JSON format.

For more parsing and output control,
see the Cue and Stream classes.

"""

import sys

from .cue import Cue
from .stream import Stream


def _read_stuff(gonzo):
    try:
        # Mpegts Video
        strm = Stream(gonzo)
        strm.decode()
        return True
    except:
        try:
            cue = Cue(gonzo)
            cue.decode()
            cue.show()
            return True
        except:
            return False


def decode(gonzo=None):
    """
    decode is a SCTE-35 decoder function
    with input type auto-detection.

    SCTE-35 data is printed in JSON format.

    Use like:

    # Base64
    gonzo = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    splicefu.decode(gonzo)

    # Bytes
    payload = b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96"
    splicefu.decode(payload)

    # Hex String
    gonzo = '0XFC301100000000000000FFFFFF0000004F253396'
    splicefu.decode(gonzo)

    # Hex Literal
    splicefu.decode(0XFC301100000000000000FFFFFF0000004F253396)

    # Integer
    big_int = 1439737590925997869941740173214217318917816529814
    splicefu.decode(big_int)

    # Mpegts File
    splicefu.decode('/path/to/mpegts')

    # Mpegts HTTP/HTTPS Streams
    splicefu.decode('https://futzu.com/xaa.ts')

    """
    if gonzo in [None, sys.stdin.buffer]:
        # Mpegts stream or file piped in
        return Stream(sys.stdin.buffer).decode()
    if isinstance(gonzo, int):
        return _read_stuff(hex(gonzo))
    return _read_stuff(gonzo)
