from socket import SOL_SOCKET, SO_BROADCAST
from threading import Thread
from typing import Optional, Union

from module.sockets.sockets import Sockets


class UDPServer(Sockets):
    def __init__(self, net_type: Sockets.IPProtocol, local_host: Optional[str] = None, local_port: int = 8888,
                 read_buffer: int = 1024, read_handler=None, broadcast: bool = False):
        super().__init__(net_type, Sockets.ConnectType.UDP, Sockets.SocketMode.Server,
                         local_host, local_port, None, None,
                         read_buffer, read_handler, True)
        self._broadcast = broadcast
        if broadcast:
            self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.thread_pool.submit(Thread(target=self._recv_data, name="UDPServerRecvThread", daemon=True).start)
        self._logger.info("UDPServerInit")

    def broadcast(self, data: Union[str, bytes], port: Optional[int] = None, encoding: Optional[str] = None):
        if not self._broadcast:
            return
        if isinstance(data, str):
            if encoding:
                data = bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode(encoding=encoding)))
            else:
                data = bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode()))
        self._logger.info(f"Broadcast message: {data}")
        self._socket.sendto(data, ("<broadcast>", port if port else self._local_addr[1]))
