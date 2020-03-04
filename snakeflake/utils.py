"""General utilities"""

import socket

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

    nums = [int(i) for i in ip_address.split(".")][::-1]

    ret = 0
    exp = 0

    bitcount /= 2

    for n in nums:
        if (exp > bitcount):
            break

        ret += n * (256 ** exp)
        exp += 1
    
    return ret