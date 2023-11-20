import time

from module.sockets.tcp_server import TCPServer

# temp = TCPClient(TCPClient.IPProtocol.IPV4, port=9999)
# temp.connect()
#
# temp.send_data("test")

if __name__ == "__main__":
    temp = TCPServer(TCPServer.IPProtocol.IPV4)
    print(temp)

    while True:
        time.sleep(0.5)
