import socket
import struct

# Extract data from frame
def frame(data):
    destination, source, protocol = struct.unpack('! 6s 6s H', data[:14]) # First 14 bytes from IP-packet. Source & Destionation = 6, protocol is 2 bytes.
    return get_mac(destination), get mac(source), socket.htons(protocol), data[14:] # Make extracted data readable and return payload (everything after 14th byte)

# Return human formatted mac
def get_mac(byte_addr):
    byte_string = map('{:02x}'.format, byte_addr) # Divide into chunks of two characters
    return ':'.join(byte_string).upper() # Join values into a colon separated uppercase MAC
