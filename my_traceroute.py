#!/usr/bin/env python3
"""
my_traceroute.py
Author: Elan A. Cote
Custom implementation of traceroute using UDP probes.
"""


import argparse
import socket
import struct
import time

MAX_TTL = 30
PORT = 33434




def traceroute(destination, numeric, queries, summary):
    """
    Perform traceroute.
    """
    dest_ip = socket.gethostbyname(destination)
    print(f"traceroute to {destination} ({dest_ip}), "
          f"{MAX_TTL} hops max")


    for ttl in range(1, MAX_TTL + 1):
        print(f"{ttl} ", end="")
        unanswered = 0


        for _ in range(queries):
            recv_sock = socket.socket(socket.AF_INET,
                                      socket.SOCK_RAW,
                                      socket.IPPROTO_ICMP)
            send_sock = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM,
                                      socket.IPPROTO_UDP)


            send_sock.setsockopt(socket.SOL_IP,
                                 socket.IP_TTL,
                                 ttl)


            recv_sock.settimeout(2)


            send_time = time.time()
            send_sock.sendto(b'', (dest_ip, PORT))


            try:
                data, addr = recv_sock.recvfrom(512)
                rtt = (time.time() - send_time) * 1000


                host = addr[0]
                if not numeric:
                    try:
                        host = socket.gethostbyaddr(addr[0])[0]
                    except socket.herror:
                        pass


                print(f"{host} ({addr[0]}) {rtt:.3f} ms ", end="")
            except socket.timeout:
                unanswered += 1
                print("* ", end="")


            finally:
                send_sock.close()
                recv_sock.close()


        if summary:
            print(f" | {unanswered} unanswered", end="")


        print()


        if addr[0] == dest_ip:
            break




def main():
    parser = argparse.ArgumentParser(description="Custom Traceroute")
    parser.add_argument("destination")
    parser.add_argument("-n", action="store_true",
                        help="Numeric output only")
    parser.add_argument("-q", type=int, default=3,
                        help="Number of probes per hop")
    parser.add_argument("-S", action="store_true",
                        help="Print summary of unanswered probes")


    args = parser.parse_args()


    traceroute(args.destination,
               args.n,
               args.q,
               args.S)




if __name__ == "__main__":
    main()
