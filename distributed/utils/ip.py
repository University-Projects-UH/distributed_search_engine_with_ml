import socket

def give_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return local_ip
