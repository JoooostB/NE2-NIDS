#!/usr/bin/sudo python
import socket
import struct
import textwrap

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
        raw, addr = connection.recvfrom(65536)  # Store to maximum buffer (65536)
        destination, source, protocol, data = eth_frame(raw)
        print('\nEthernet Frame:')
        print('\t - Destination: {}, Source: {}, Protocol: {}'.format(destination, source, protocol, data)) # Fill placeholders {} with data

        if protocol == 8:    # If protocol is IPv4
            (version, IHL, ttl, protocol, source, destination, data) = ip_packet(data)
            print('IPv4 Packet:')
            print('\t\t - Version: {}, Header Length: {}, TTL: {}'.format(version, IHL, ttl))
            print('\t\t - Protocol: {}, Source: {}, Destination: {}'.format(protocol, source, destination))

            if protocol == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print('\t - ICMP Packet:')
                print('\t\t - Type: {}, Code: {}, Checksum: {}'.format(icmp_type, code, checksum))
                print('\t\t - Data:')
                print(format_multi_line('\t\t\t   ', data))

            elif protocol == 6:
                (src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
                print('\t - TCP Segment:')
                print('\t\t - Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                print('\t\t - Sequence: {}, Acknowledgment: {}'.format(sequence, acknowledgment))
                print('\t\t - Flags:')
                print('\t\t\t -  URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN:{}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print('\t\t - Data:')
                print(format_multi_line('\t\t\t ', data))

            elif protocol == 17:
                src_port, dest_port, length, data = udp_segment(data)
                print('\t - UDP Segment:')
                print('\t\t - Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))

            else:
                print('\t - Data:')
                print(format_multi_line('\t\t ', data))

        else:
            print('Data:')
            print(format_multi_line('\t ', data))


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
    ttl, protocol, source, destination = struct.unpack('! 8x B B 2x 4s 4s', data[:20])  # Format data is packed into
    return version, IHL, ttl, protocol, ipv4(source), ipv4(destination), data[IHL:]  # Data is everything after the header


#  Return human readable IPv4
def ipv4(raw_addr):
    return '.'.join(map(str, raw_addr))


# Extract UDP packet
def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8]) # grab first 8 bytes (header) of the UDP packet
    return src_port, dest_port, size, data[8:]


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


main()