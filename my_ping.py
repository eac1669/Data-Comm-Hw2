#!/usr/bin/env python3
"""
my_ping.py


A custom implementation of the Linux ping utility using raw sockets.
"""


import argparse
import os
import socket
import struct
import sys
import time
import select
import statistics




ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
DEFAULT_DATA_SIZE = 56




def checksum(source_string):
    """
    Calculate ICMP checksum.
    """
    sum_ = 0
    count_to = (len(source_string) // 2) * 2


    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum_ += this_val
        sum_ &= 0xffffffff
        count += 2


    if count_to < len(source_string):
        sum_ += source_string[len(source_string) - 1]
        sum_ &= 0xffffffff


    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ += (sum_ >> 16)
    answer = ~sum_ & 0xffff
    answer = socket.htons(answer)


    return answer




def create_packet(identifier, sequence, size):
    """
    Create ICMP echo request packet.
    """
    header = struct.pack("!BBHHH",
                         ICMP_ECHO_REQUEST,
                         0,
                         0,
                         identifier,
                         sequence)


    data = bytes(size)
    chksum = checksum(header + data)


    header = struct.pack("!BBHHH",
                         ICMP_ECHO_REQUEST,
                         0,
                         chksum,
                         identifier,
                         sequence)


    return header + data




def receive_packet(sock, identifier, timeout):
    """
    Receive ICMP reply packet.
    """
    start_time = time.time()


    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0] == []:
            return None


        time_received = time.time()
        packet, addr = sock.recvfrom(1024)


        icmp_header = packet[20:28]
        icmp_type, code, _, packet_id, sequence = struct.unpack("!BBHHH", icmp_header)


        if icmp_type == ICMP_ECHO_REPLY and packet_id == identifier:
            return time_received - start_time


        timeout -= (time_received - start_time)
        if timeout <= 0:
            return None




def ping(destination, count, interval, size, timeout):
    """
    Perform ping operation.
    """
    try:
        dest_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        print("Cannot resolve host:", destination)
        sys.exit(1)


    print(f"PING {destination} ({dest_ip}) {size} bytes of data.")


    identifier = os.getpid() & 0xFFFF
    rtts = []


    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_RAW,
                         socket.IPPROTO_ICMP)


    start_time = time.time()
    sequence = 1
    sent = 0
    received = 0


    while True:
        if count and sequence > count:
            break
        if timeout and (time.time() - start_time) > timeout:
            break


        packet = create_packet(identifier, sequence, size)
        sock.sendto(packet, (dest_ip, 1))
        sent += 1


        rtt = receive_packet(sock, identifier, 1)


        if rtt is None:
            print("Request timeout for icmp_seq", sequence)
        else:
            received += 1
            rtts.append(rtt * 1000)
            print(f"{size + 8} bytes from {dest_ip}: "
                  f"icmp_seq={sequence} time={rtt * 1000:.3f} ms")


        sequence += 1
        time.sleep(interval)


    print("\n--- {} ping statistics ---".format(destination))
    loss = ((sent - received) / sent) * 100
    print(f"{sent} packets transmitted, {received} received, "
          f"{loss:.1f}% packet loss")


    if rtts:
        print("rtt min/avg/max = "
              f"{min(rtts):.3f}/{statistics.mean(rtts):.3f}/"
              f"{max(rtts):.3f} ms")




def main():
    parser = argparse.ArgumentParser(description="Custom Ping")
    parser.add_argument("destination")
    parser.add_argument("-c", type=int, help="Number of packets")
    parser.add_argument("-i", type=float, default=1,
                        help="Interval between packets")
    parser.add_argument("-s", type=int, default=DEFAULT_DATA_SIZE,
                        help="Packet size")
    parser.add_argument("-t", type=int, help="Timeout in seconds")


    args = parser.parse_args()


    ping(args.destination,
         args.c,
         args.i,
         args.s,
         args.t)




if __name__ == "__main__":
    main()
