# A Simple UDP class

# from email.headerregistry import Address
import socket

class UDP(object):
    """simple UDP ping class"""
    handle = None   # Socket for send/recv
    port = 0        # UDP port we work on
    broadcast = ''  # Broadcast address

    def __init__(self, port, broadcast=None):
        if broadcast is None:
            broadcast = '255.255.255.255'

        self.broadcast = broadcast
        self.port = port
        # Create UDP socket
        self.handle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # to udplib3.py
        # Allow multiple processes to bind to socket; incoming
        # messages will come to each process
        self.handle.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # TO-DO: Multicast support

        # Ask operating system to let us do broadcasts from socket
        self.handle.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Bind UDP socket to local port so we can receive pings
        self.handle.bind(('', port))

    def send(self, buf):
        """
        Send broadcast message 'buf'
        """
        self.handle.sendto(buf, 0, (self.broadcast, self.port))

    def recv(self, n):
        """
        Recive messages
        Return: message, (address, port)
        """
        buf, addrinfo = self.handle.recvfrom(n)
        return buf.decode('utf-8'), addrinfo
