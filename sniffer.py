#!/usr/bin/sudo python
import json
import os
import requests
import socket
import struct
import sys
import textwrap

from collector.models import Database as DB

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
    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))  # Change AF_INET to AF_PACKET when running under Linux and vise versa
    while True:
        (source, destination, protocol, version, IHL, ttl, ip_protocol, ip_source, ip_destination,
         icmp_type, icmp_code, icmp_checksum, icmp_data, udp_src_port, udp_dest_port, udp_length,
         tcp_sequence, tcp_acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = \
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'

        raw, addr = connection.recvfrom(65536)  # Store to maximum buffer (65536)
        destination, source, protocol, data = eth_frame(raw)
        print('\nEthernet Frame:')
        print('\t - Destination: {}, Source: {}, Protocol: {}'.format(destination, source, protocol, data)) # Fill placeholders {} with data
        if protocol == 8:    # If protocol is IPv4
            (version, IHL, ttl, ip_protocol, ip_source, ip_destination, data) = ip_packet(data)
            print('IPv4 Packet:')
            print('\t\t - Version: {}, Header Length: {}, TTL: {}'.format(version, IHL, ttl))
            print('\t\t - Protocol: {}, Source: {}, Destination: {}'.format(protocol, ip_source, ip_destination))

            if protocol == 1:
                (icmp_type, icmp_code, icmp_checksum, icmp_data) = icmp_packet(data)
                print('\t - ICMP Packet:')
                print('\t\t - Type: {}, Code: {}, Checksum: {}'.format(icmp_type, icmp_code, icmp_checksum))
                print('\t\t - Data:')
                print(format_multi_line('\t\t\t   ', icmp_data))

            elif protocol == 6:
                (src_port, dest_port, tcp_sequence, tcp_acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
                print('\t - TCP Segment:')
                print('\t\t - Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                print('\t\t - Sequence: {}, Acknowledgment: {}'.format(tcp_sequence, tcp_acknowledgment))
                print('\t\t - Flags:')
                print('\t\t\t -  URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN:{}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print('\t\t - Data:')
                print(format_multi_line('\t\t\t ', data))

            elif protocol == 17:
                (udp_src_port, udp_dest_port, udp_length, data) = udp_segment(data)
                print('\t - UDP Segment:')
                print('\t\t - Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, udp_length))

            else:
                print('\t - Data:')
                print(format_multi_line('\t\t ', data))

        else:
            print('Data:')
            print(format_multi_line('\t ', data))

        # POST-request to send to collector

        dict_to_send = {'packet':
                        {'ip': ip_source,
                         'protocol': ip_protocol,
                         'bytes': udp_length
                         }
                        }

        # Url
        url = "http://localhost:5000/insert_packet"

        # Send request
        res = requests.post(url, data=json.dumps(dict_to_send))

        # Get response
        dict_from_server = res.json()
        print("response from server:", dict_from_server)


#  Extract data from frame
def eth_frame(data):
    destination, source, protocol = struct.unpack('! 6s 6s H', data[:14])  # First 14 bytes from IP-packet. Source & Destination = 6, protocol is 2 bytes.
    return get_mac(destination), get_mac(source), socket.htons(protocol), data[14:]  # Make extracted data readable and return payload (everything after 14th byte)


#  Return human readable mac
def get_mac(bytes_addr):
    byte_string = map('{:02x}'.format, bytes_addr)  # Divide into chunks of two characters
    mac_addr = ':'.join(byte_string).upper()    # Join values into a colon separated uppercase MAC
    return mac_addr


#  Extract IPv4 packet
def ip_packet(data):
    version_IHL = data[0]  # Grabs version and Head Length from IP Header
    version = version_IHL >> 4  # Bit shift 4 bits to remove IHL (add 4 zero's)
    IHL = (version_IHL & 15) * 4  # Get last 4 bits of first byte
    ttl, ip_protocol, source, destination = struct.unpack('! 8x B B 2x 4s 4s', data[:20])  # Format data is packed into
    return version, IHL, ttl, ip_protocol, ipv4(source), ipv4(destination), data[IHL:]  # Data is everything after the header


#  Return human readable IPv4
def ipv4(raw_addr):
    return '.'.join(map(str, raw_addr))


# Extract UDP packet
def udp_segment(data):
    udp_src_port, udp_dest_port, udp_length = struct.unpack('! H H 2x H', data[:8]) # grab first 8 bytes (header) of the UDP packet
    return udp_src_port, udp_dest_port, udp_length, data[8:]


# Extract ICMP (ping) packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])  # grab first 4 bytes (header) of the ICMP packet
    return icmp_type, code, checksum, data[4:]  # Add data, everything after 4th byte


# Extract TCP segment based on the TCP IP packet diagram
def tcp_segment(data):
    (src_port, dest_port, sequence, acknowledgment,
     offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])

    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1

    return (src_port, dest_port, sequence, acknowledgment, flag_urg,
            flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:])


# Format multi line output
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        db = DB()
        db.clear()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
