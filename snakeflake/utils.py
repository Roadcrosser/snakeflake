"""General utilities"""

import socket
import datetime
import math


def get_ip(dummy_ip="192.168.0.1"):
    """Gets your IP address
    
    This is done by pinging a dummy IP.

    Args:
        dummy_ip (str): The IP(v4) address to ping to get your IP(v4) address. Defaults to `192.169.0.1`.

    Returns:
        str: Your IP address.
    """

    # TODO: IPv6 support
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ip_address = "127.0.0.1"

    try:
        sock.connect((dummy_ip, 1))
        ip_address = sock.getsockname()[0]
    finally:
        sock.close()

    return ip_address


def ipv4_to_int(ip_address, bitcount):
    """Converts an IPv4 address into an integer with the specified number of bits.
    
    This number used for the Machine ID if none is specified.
    
    Args:
        ip_address (str): Your IP(v4) address.
        bitcount (int): The upper limit of bits allowed.

    Returns:
        int: The converted number.
    
    """

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
    """Formats an error message with the provided worker ID."""
    return f"Worker {worker_id}: {message}"


def world_epoch():
    """Returns the datetime of the epoch.

    Returns:
        datetime.datetime: The epoch datetime.
    """
    return datetime.datetime.fromtimestamp(0)


def bitfill(num):
    """Fills a number of bits with 1.

    Args:
        num (int): The number of bits to fill.

    Returns:
        int: The filled bits.
    """
    return sum(2 ** i for i in range(num))


def timestamp_to_microseconds(ts):
    """Converts a datetime object to the number of microseconds since epoch.

    Args:
        ts (datetime.datetime): The datetime object.
    
    Returns:
        int: The number of microseconds from epoch.
    """
    microsecond_amount = 1000000  # 1 second worth of microseconds
    return ts.timestamp() * microsecond_amount
