#!/usr/bin/sudo python
import socket
import struct


def main():
    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))  # Change AF_INET to AF_PACKET when running under Linux
    while True:
        raw, addr = connection.recvfrom(65536)  # Store to maximum buffer
        destination, source, protocol, data = eth_frame(raw)
        print('\nEthernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(destination, source, protocol, data)) # Fill placeholders {} with data

# Extract data from frame
def eth_frame(data):
    destination, source, protocol = struct.unpack('! 6s 6s H', data[:14]) # First 14 bytes from IP-packet. Source & Destionation = 6, protocol is 2 bytes.
    return get_mac(destination), get_mac(source), socket.htons(protocol), data[14:] # Make extracted data readable and return payload (everything after 14th byte)


# Return human formatted mac
def get_mac(byte_addr):
    byte_string = map('{:02x}'.format, byte_addr) # Divide into chunks of two characters
    return ':'.join(byte_string).upper() # Join values into a colon separated uppercase MAC


main()