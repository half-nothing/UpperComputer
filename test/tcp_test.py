import time

from module.sockets.tcp_client import TCPClient
from module.sockets.tcp_server import TCPServer

# temp = TCPClient(TCPClient.IPProtocol.IPV4, local_port=8888, remote_host="192.168.137.97", remote_port=2222)
#
# temp.send_data("test")
#
# while True:
#     time.sleep(0.5)

temp = TCPServer(TCPServer.IPProtocol.IPV4, local_port=8888)

while True:
    time.sleep(0.5)
    print(temp)
