#!/usr/bin/sudo python
import socket
import struct

'''
IP Protocol ID's
1 ICMP  50 ESP
2 IGMP  51 AH
6 TCP   57 SKIP
9 IGRP  88 EIGRP
17 UDP  89 OSPF
47 GRE  115 L2TP
'''

def main():
    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))  # Change AF_INET to AF_PACKET when running under Linux
    while True:
        raw, addr = connection.recvfrom(65536)  # Store to maximum buffer
        destination, source, protocol, data = eth_frame(raw)
        print('\nEthernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(destination, source, protocol, data)) # Fill placeholders {} with data

#  Extract data from frame
def eth_frame(data):
    destination, source, protocol = struct.unpack('! 6s 6s H', data[:14])  # First 14 bytes from IP-packet. Source & Destination = 6, protocol is 2 bytes.
    return get_mac(destination), get_mac(source), socket.htons(protocol), data[14:]  # Make extracted data readable and return payload (everything after 14th byte)


#  Return human readable mac
def get_mac(byte_addr):
    byte_string = map('{:02x}'.format, byte_addr)  # Divide into chunks of two characters
    return ':'.join(byte_string).upper()  # Join values into a colon separated uppercase MAC

#  Extract IPv4 packet
def ip_packet(data):
    version_IHL = data[0]  # Grabs version and Head Length from IP Header
    version = version_IHL >> 4  # Bit shift 4 bits to remove IHL (add 4 zero's)
    IHL = (version_IHL & 15) * 4  # Get last 4 bits of first byte
    ttl, protocol, source, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])  # Format data is packed into
    return version, IHL, ttl, protocol, ipv4(source), ipv4(target), data[IHL:]  # Data is everything after the header

#  Return human readable IPv4
def ipv4(raw_addr):
    return '.'.join(map(str, raw_addr))

main()
