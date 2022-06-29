import time
import signal
import zmq
from udplib import UDP

print("something")

PING_PORT_NUMBER = 2525
PING_MSG_SIZE    = 1
PING_INTERVAL    = 1  # Once per second

def main():

    udp = UDP(PING_PORT_NUMBER)

    poller = zmq.Poller()
    poller.register(udp.handle, zmq.POLLIN)

    # Send first ping right away
    ping_at = time.time()

    while True:
        timeout = ping_at - time.time()
        if timeout < 0:
            timeout = 0
        try:
            events = dict(poller.poll(1000* timeout))
        except KeyboardInterrupt or signal.SIGTERM:
            print("interrupted")
            break

        # Someone answered our ping
        if udp.handle.fileno() in events:
            resp, addrinfo = udp.recv(PING_MSG_SIZE)
            if addrinfo[0] != udp.address:
                if(resp == 's'):
                    print("Found server %s:%d" % addrinfo)
                else:
                    print("Found peer %s:%d" % addrinfo)

        if time.time() >= ping_at:
            # Broadcast our beacon
            print ("Pinging peers...")
            udp.send(b'!')
            ping_at = time.time() + PING_INTERVAL

if __name__ == '__main__':
    main()
