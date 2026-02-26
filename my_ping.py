#!/usr/bin/env python3

import argparse
import os
import socket
import struct
import sys
import time
import select

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0


def checksum(data):
    s = 0
    for i in range(0, len(data) - 1, 2):
        s += (data[i] << 8) + data[i + 1]
    if len(data) % 2:
        s += data[-1] << 8
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff


def create_packet(pid, seq):
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, pid, seq)
    data = b'abcdefghijklmnopqrstuvwabcdefghi'  # 32 bytes
    chksum = checksum(header + data)
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, chksum, pid, seq)
    return header + data


def receive_ping(sock, pid):
    start = time.time()
    while True:
        ready = select.select([sock], [], [], 1)
        if not ready[0]:
            return None
        recv_time = time.time()
        packet, _ = sock.recvfrom(1024)
        icmp_header = packet[20:28]
        icmp_type, _, _, packet_id, seq = struct.unpack("!BBHHH", icmp_header)
        if icmp_type == ICMP_ECHO_REPLY and packet_id == pid:
            return (recv_time - start) * 1000


def ping(dest, count):
    try:
        dest_ip = socket.gethostbyname(dest)
    except socket.gaierror:
        print("Cannot resolve host")
        sys.exit(1)

    print(f"PING {dest} ({dest_ip})")

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    pid = os.getpid() & 0xFFFF

    seq = 1
    sent = received = 0

    while count is None or seq <= count:
        packet = create_packet(pid, seq)
        sock.sendto(packet, (dest_ip, 1))
        sent += 1

        rtt = receive_ping(sock, pid)

        if rtt is None:
            print(f"Request timeout for icmp_seq {seq}")
        else:
            received += 1
            print(f"Reply from {dest_ip}: icmp_seq={seq} time={rtt:.2f} ms")

        seq += 1
        time.sleep(1)

    print(f"\n{sent} packets transmitted, {received} received")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("-c", type=int, help="Number of packets")
    args = parser.parse_args()

    ping(args.destination, args.c)


if __name__ == "__main__":
    main()