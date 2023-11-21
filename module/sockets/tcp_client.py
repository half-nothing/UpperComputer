from socket import SOL_SOCKET, SO_KEEPALIVE
from threading import Thread
from typing import Optional

from module.sockets.sockets import Sockets


class TCPClient(Sockets):
    def __init__(self, net_type: Sockets.IPProtocol, host: Optional[str] = None, port: Optional[int] = 8888,
                 read_buffer: int = 1024, read_handler=None):
        super().__init__(net_type, Sockets.ConnectType.TCP, Sockets.SocketMode.Client,
                         host, port, read_buffer, read_handler)
        self.connect(self._bind_host, self._bind_port)
        self._socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        self.thread_pool.submit(Thread(target=self._recv_data, name="TCPClientRecvThread", daemon=True).start)
        self._logger.info("TCPClientInit")
