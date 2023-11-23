from threading import Thread
from typing import Optional

from module.sockets.sockets import Sockets


class UDPClient(Sockets):
    def __init__(self, net_type: Sockets.IPProtocol, local_port: int = 8888, remote_host: Optional[str] = None,
                 remote_port: int = 8888, read_buffer: int = 1024, read_handler=None):
        super().__init__(net_type, self.ConnectType.UDP, Sockets.SocketMode.Client,
                         None, local_port, remote_host, remote_port,
                         read_buffer, read_handler, True)
        self.thread_pool.submit(Thread(target=self._recv_data, name="UDPClientRecvThread", daemon=True).start)
        self._logger.info("UDPClientInit")
