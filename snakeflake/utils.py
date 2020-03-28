"""General utilities"""

import socket
import datetime
import math


def get_ip():
    """Gets your IP address"""

    # TODO: IPv6 support
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ip_address = "127.0.0.1"

    dummy_ip = "192.168.0.1"
    try:
        sock.connect((dummy_ip, 1))
        ip_address = sock.getsockname()[0]
    finally:
        sock.close()

    return ip_address


def ipv4_to_int(ip_address, bitcount):
    """Converts an IPv4 address into an integer with the specified number of bits"""

    ip_split = [int(i) for i in ip_address.split(".")]

    ret = 0

    to_shift = 8

    for n in ip_split:
        ret = ret << to_shift
        ret += n

    bits = (1 << bitcount) - 1

    ret = ret & bits
    return ret


def format_error(worker_id, message):
    return f"Worker {worker_id}: {message}"


def world_epoch():
    return datetime.datetime.fromtimestamp(0)


def bitfill(num):
    return sum(2 ** i for i in range(num))


def timestamp_to_microseconds(ts):
    microsecond_amount = 1000000  # 1 second worth of microseconds
    return ts.timestamp() * microsecond_amount
