from threading import Thread
from typing import Optional

from module.sockets.sockets import Sockets


class UDPClient(Sockets):
    def __init__(self, net_type: Sockets.IPProtocol, host: Optional[str] = None, port: Optional[int] = 8888,
                 read_buffer: int = 1024, read_handler=None, broadcast: bool = False):
        super().__init__(net_type, self.ConnectType.UDP, Sockets.SocketMode.Client,
                         host, port, read_buffer, read_handler)
        self._broadcast = broadcast
        if broadcast:
            self._socket.bind(("0.0.0.0", self._bind_port))
        self.thread_pool.submit(Thread(target=self._recv_data, name="UDPClientRecvThread", daemon=True).start)
