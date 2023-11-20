from socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket
from threading import Thread
from typing import Optional

from module.sockets.sockets import Sockets


class TCPServer(Sockets):

    def __init__(self, net_type: Sockets.IPProtocol, listen_number: int = 4,
                 host: Optional[str] = None, port: Optional[int] = 8888, read_buffer: int = 1024, read_handler=None):
        super().__init__(net_type, Sockets.ConnectType.TCP, Sockets.SocketMode.Server,
                         host, port, read_buffer, read_handler)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind((self._bind_host, self._bind_port))
        self._socket.listen(listen_number)
        self._clients = set()
        self.thread_pool.submit(Thread(target=self._main_loop, name="TCPServerMainThread", daemon=True).start)
        self._logger.info("TCPServerInit")

    def _main_loop(self):
        while True:
            soc, addr = self._socket.accept()
            self._logger.info(f"New connection from {addr[0]}:{addr[1]}")
            self._clients.add(soc)
            self.thread_pool.submit(
                Thread(target=self._recv_data_loop, name="TCPRecvDataThread", args=(soc, addr), daemon=True).start)

    def _recv_data_loop(self, soc: socket, addr: tuple[str, int]):
        while True:
            data = soc.recv(self._read_buffer)
            if data == b'':
                self._logger.info(f"{addr[0]}:{addr[1]} disconnect")
                self._clients.remove(soc)
                break
            if self._read_handler:
                self._read_handler(data, addr)
            else:
                print("Received:", repr(data), "from", addr)
