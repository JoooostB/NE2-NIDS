import socket
import struct

# Extract data from frame
def frame(data):
    destination, source, protocol = struct.unpack('! 6s 6s H', data[:14]) # First 14 bytes from IP-packet. Source & Destionation = 6, protocol is 2 bytes.
    return get_mac(destination), get mac(source), socket.htons(protocol), data[14:] # Make extracted data readable and return payload (everything after 14th byte)

