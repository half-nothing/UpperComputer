from threading import Thread
from typing import Optional

from module.sockets.sockets import Sockets


class TCPClient(Sockets):
    def __init__(self, net_type: Sockets.IPProtocol, local_port: Optional[int] = 8888,
                 remote_host: Optional[str] = None, remote_port: Optional[int] = 8888, read_buffer: int = 1024,
                 read_handler=None) -> None:
        super().__init__(net_type, Sockets.ConnectType.TCP, Sockets.SocketMode.Client,
                         None, local_port, remote_host, remote_port,
                         read_buffer, read_handler, True)
        if not self.connect():
            self._socket.close()
            self._logger.clear()
            raise ConnectionError(self.remote_address)
        self.thread_pool.submit(Thread(target=self._recv_data, name="TCPClientRecvThread", daemon=True).start)
        self._logger.info(f"TCPClientInit, remote: {self.remote_address}, local: {self.local_address}")
