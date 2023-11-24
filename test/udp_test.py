import time

from module.sockets.udp_server import UDPServer

# temp = UDPClient(UDPClient.IPProtocol.IPV4, read_buffer=40000, port=8888)
# print(temp)
# temp.connect()
# while True:
#     temp.send_data("test")
#     time.sleep(0.5)
#
temp = UDPServer(UDPServer.IPProtocol.IPV4, broadcast=True)
print(temp)

while True:
    temp.broadcast("broadcast", 8080)
    time.sleep(0.5)
    pass
