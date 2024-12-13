"""
new_reader.py
Home of the reader function
"""

import socket
import struct
import sys
import urllib.request


TIMEOUT = 60


def reader(uri, headers={}):
    """
    reader returns an open file handle.
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
     (http headers can be added by setting headers)
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"

    Use like:

    with reader('http://iodisco.com/') as disco:
        disco.read()

    with reader('http://iodisco.com/',headers={"myHeader":"DOOM"}) as doom:
        doom.read()

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)

    with reader("/home/you/video.ts") as data:
        fu = data.read()

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()

    """
    # read from stdin
    if uri in [None, sys.stdin.buffer]:
        return sys.stdin.buffer
    # Multicast
    if uri.startswith("udp://@"):
        return _open_mcast(uri)
    # Udp
    if uri.startswith("udp://"):
        return _open_udp(uri)
    # Http(s)
    if uri.startswith("http"):
        req = urllib.request.Request(uri, headers=headers)
        return urllib.request.urlopen(req)
    # File
    return open(uri, "rb")


def _read_stream(sock):
    """
    return a socket that can be read like a file.
    """
    return sock.makefile(mode="rb")


def double_rcvbuf(sock):
    """
    double_rcvbuf doubles socket.SO_RCVBUF
    until it errors
    """
    rcvbuf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"\nReading rcvbuf_size of {rcvbuf_size}", file=sys.stderr)
    while True:
        try:
            rcvbuf_size += rcvbuf_size
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcvbuf_size)
        except:
            print(f"Setting rcvbuf_size to {rcvbuf_size}\n\n", file=sys.stderr)
            break


def _mk_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    double_rcvbuf(sock)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    return sock


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    udp_sock = _mk_sock()
    udp_sock.bind((udp_ip, udp_port))
    return _read_stream(udp_sock)


def _open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).rsplit(":", 1)
    udp_port = int(udp_port)
    return _mk_udp_sock(udp_ip, udp_port)


def _open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """

    class Socked(socket.socket):
        def read(self, bites):
            return self.recv(bites)

    interface_ip = "0.0.0.0"
    multicast_group, port = (uri.split("udp://@")[1]).rsplit(":", 1)
    multicast_port = int(port)
    socked = Socked(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", 32))
    socked.bind(("", multicast_port))
    socked.setsockopt(
        socket.SOL_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(multicast_group) + socket.inet_aton(interface_ip),
    )
    socked.settimeout(TIMEOUT)
    return socked
