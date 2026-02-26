# Data-Comm-Hw2

Custom ping and traceroute Implementation (WSL)
Overview
This project contains:
my_ping.py — A custom implementation of the Linux ping utility using raw ICMP sockets.


my_traceroute.py — A custom implementation of traceroute using UDP probes and ICMP replies.


Both programs were developed and tested inside WSL (Windows Subsystem for Linux) using Visual Studio Code.
How to Compile and Run

Requirements
WSL (Ubuntu recommended)


Python 3 installed


Root privileges (required for raw sockets)


To verify Python:
python3 --version

If not installed:
sudo apt update
sudo apt install python3
Both programs use raw sockets, so they must be run with sudo
How to Run my_ping.py
Basic Syntax
sudo python3 my_ping.py <destination> [options]
Arguments
Option
Description
destination
Hostname or IP address
-c <count>
 Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified, ping will operate until interrupted.
-i <interval>
Wait for wait seconds between sending each packet. Default is one second.
-s <size>
Specify the number of data bytes to be sent. Default is 56 (64 ICMP data bytes including the header).
-t <timeout>
Specify a timeout in seconds before ping exits regardless of how many packets have been received




Example Usage
Ping indefinitely (until Ctrl+C)
sudo python3 my_ping.py google.com

Send 4 packets only
sudo python3 my_ping.py google.com -c 4

Send 5 packets with 0.5 second interval
sudo python3 my_ping.py google.com -c 5 -i 0.5

Use custom packet size
sudo python3 my_ping.py google.com -s 128

How to Run my_traceroute.py
Basic Syntax
sudo python3 my_traceroute.py <destination> [options]
Arguments
Option
Description
destination
Hostname or IP address
-n
Print hop addresses numerically rather than symbolically and numerically.
-q <n>
Set the number of probes per TTL to n queries
-S
Print a summary of how many probes were not answered for each hop


Example Usage
Standard traceroute
sudo python3 my_traceroute.py google.com

Numeric output only
sudo python3 my_traceroute.py google.com -n

5 probes per hop
sudo python3 my_traceroute.py google.com -q 5

Show unanswered probe summary
sudo python3 my_traceroute.py google.com -S

Running Inside VS Code (WSL)
If using Visual Studio Code:
Open WSL terminal.


Navigate to the project directory.


Run:


code .
Open the integrated terminal in VS Code.


Execute commands using sudo python3 ....
Notes
Both programs require root privileges because raw sockets are used.


These programs were tested on Ubuntu under WSL.


Execution outside WSL (e.g., Windows PowerShell) may fail unless run as Administrator.
