from socket import socket
from threading import Thread
from typing import Optional, Union

from module.sockets.sockets import Sockets


class TCPServer(Sockets):
    _connect_handler = None
    _disconnect_handler = None

    def __init__(self, net_type: Sockets.IPProtocol, listen_number: int = 4,
                 local_host: Optional[str] = None, local_port: Optional[int] = 8888, read_buffer: int = 1024,
                 read_handler=None, connect_handler=None, disconnect_handler=None) -> None:
        super().__init__(net_type, Sockets.ConnectType.TCP, Sockets.SocketMode.Server,
                         local_host, local_port, None, None,
                         read_buffer, read_handler, True)
        self._socket.listen(listen_number)
        self._connect_handler, self._disconnect_handler = connect_handler, disconnect_handler
        self._clients = {}
        self.thread_pool.submit(Thread(target=self._main_loop, name="TCPServerMainThread", daemon=True).start)
        self._logger.info(f"TCPServerInit, listen: {self.local_address}")

    def send_data_to(self, data: Union[str, bytes], host: Optional[Union[tuple[str, int], str]] = None,
                     port: Optional[int] = None, encoding: Optional[str] = None) -> bool:
        if isinstance(host, str):
            host = (host if host else self._remote_addr[0], port if port else self._remote_addr[1])
        host = self._get_address(host)
        if host not in self._clients.keys():
            return False
        self._logger.info(f"Send {data} to {host}")
        self._clients[host].send(self.decode_data(data, encoding))
        return True

    def _main_loop(self) -> None:
        while True:
            soc, addr = self._socket.accept()
            self._logger.info(f"New connection from {self._get_address(addr)}")
            self._clients[self._get_address(addr)] = soc
            if self._connect_handler:
                self._connect_handler(addr)
            self.thread_pool.submit(
                Thread(target=self._recv_data_loop, name="TCPRecvDataThread", args=(soc, addr), daemon=True).start)

    def _recv_data_loop(self, soc: socket, addr: tuple[str, int]) -> None:
        while True:
            try:
                data = soc.recv(self._read_buffer)
                if data == b'':
                    self._logger.info(f"{self._get_address(addr)} disconnect")
                    self._clients[self._get_address(addr)].close()
                    if self._disconnect_handler:
                        self._disconnect_handler(addr)
                    del self._clients[self._get_address(addr)]
                    break
                if self._read_handler:
                    self._read_handler(data, addr)
                else:
                    print(f"Received: {repr(data)} from {self._get_address(addr)}")
            except ConnectionResetError:
                self._logger.info(f"{self._get_address(addr)} disconnect")
                self._clients[self._get_address(addr)].close()
                if self._disconnect_handler:
                    self._disconnect_handler(addr)
                del self._clients[self._get_address(addr)]
                break
