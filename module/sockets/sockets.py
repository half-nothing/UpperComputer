from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from re import Pattern, compile
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM, socket, IPPROTO_TCP, IPPROTO_UDP
from typing import Optional, Union

from module.utils.logger import Logger


class Sockets:
    class IPProtocol(Enum):
        IPV4 = AF_INET
        IPV6 = AF_INET6

    class SocketMode(Enum):
        Client = "Client"
        Server = "Server"

    class ConnectType(Enum):
        TCP = ("TCP", SOCK_STREAM, IPPROTO_TCP)
        UDP = ("UDP", SOCK_DGRAM, IPPROTO_UDP)

    _matcher: Pattern = compile(r"\b(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})(\.(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})){3}\b")
    _socket_thread_pool: ThreadPoolExecutor = ThreadPoolExecutor()
    _socket: Optional[socket] = None
    _clients: Optional[set[socket]] = None
    _connect: bool = False
    _net_type: IPProtocol
    _mode: SocketMode
    _connect_type: ConnectType
    _bind_host: str
    _bind_port: int
    _read_buffer: int
    _read_handler = None
    _broadcast: bool = False
    _logger: Logger

    def __init__(self, net_type: IPProtocol, connect_protocol: ConnectType, mode: SocketMode,
                 host: Optional[str] = None, port: Optional[int] = 8888, read_buffer: int = 1024, read_handler=None):
        if net_type not in self.IPProtocol or connect_protocol not in self.ConnectType:
            raise Exception("参数错误")
        if mode == Sockets.SocketMode.Client:
            self._bind_host = host if host else ("127.0.0.1" if net_type == self.IPProtocol.IPV4 else "::1")
        else:
            self._bind_host = host if host else ("0.0.0.0" if net_type == self.IPProtocol.IPV4 else "::")
        self._bind_port, self._net_type, self._read_buffer, self._mode = port, net_type, read_buffer, mode
        self._net_type, self._connect_type = net_type, connect_protocol
        self._read_handler = read_handler
        self._socket = socket(self._net_type.value, self._connect_type.value[1], self._connect_type.value[2])
        self._logger = Logger(f"Sockets_{self._bind_host}_{self._connect_type.value[0]}")

    def __del__(self):
        self._socket.close()
        self.thread_pool.shutdown()
        if self._clients:
            for s in self._clients:
                s.shutdown(0)
                s.close()

    def __repr__(self):
        res = f"{'-' * 30}\n"
        res += f"Socket Mode: {self._mode.value}\n"
        if self._mode == self.SocketMode.Client and self._connect_type == self.ConnectType.TCP:
            res += f"Connect Status: {self._connect}\n"
        res += f"Connect Protocol: {self._connect_type.value[0]}\n"
        res += f"IP Protocol: {'IPV4' if self._net_type == self.IPProtocol.IPV4 else 'IPV6'}\n"
        if self._broadcast and self._mode == self.SocketMode.Server:
            res += f"{'-' * 15}\n"
            res += f"Broadcast: True\n"
            res += f"{'Connect' if self._mode == self.SocketMode.Client else 'Listen'} Port: {self._bind_port}\n"
            res += f"{'-' * 15}\n"
        res += f"{'Connect' if self._mode == self.SocketMode.Client else 'Listen'} Host: {self._bind_host}\n"
        res += f"{'Connect' if self._mode == self.SocketMode.Client else 'Listen'} Port: {self._bind_port}\n"
        if self._mode == self.SocketMode.Server and self._connect_type == self.ConnectType.TCP:
            res += f"Connect clients: {len(self._clients)}\n"
        res += f"{'-' * 30}"
        return res

    @property
    def thread_pool(self):
        return Sockets._socket_thread_pool

    @staticmethod
    def decode_data(data: str, encoding: Optional[str] = None):
        if not isinstance(data, str):
            return
        if encoding:
            return bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode(encoding=encoding)))
        else:
            return bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode()))

    def send_data(self, data: Union[str, bytes], encoding: Optional[str] = None):
        if self._connect_type == self.ConnectType.TCP and not self._connect or self._broadcast:
            self._logger.error("套接字未连接")
            return
        self._socket.send(self.decode_data(data, encoding))

    def send_data_to(self, data: Union[str, bytes], host: str, port: int, encoding: Optional[str] = None):
        if self._connect_type == self.ConnectType.UDP and not self._connect:
            self._socket.sendto(self.decode_data(data, encoding), (host, port))

    def connect(self, host: Optional[str] = None, port: Optional[int] = None):
        if self._connect or self._broadcast:
            return
        self._socket.connect((host if host else self._bind_host, port if port else self._bind_port))
        self._connect = True

    def disconnect(self):
        if not self._connect:
            return
        if self._connect_type == self.ConnectType.TCP:
            self._socket.shutdown(0)
        self._socket.close()

    def _recv_data(self):
        while True:
            try:
                if self._connect_type == self.ConnectType.UDP:
                    try:
                        data, addr = self._socket.recvfrom(self._read_buffer)
                        if self._read_handler:
                            self._read_handler(data, addr)
                        else:
                            self._logger.debug(f"Received: {repr(data)}, from {addr}")
                    except ConnectionResetError:
                        continue
                else:
                    try:
                        if not self._connect:
                            continue
                        data = self._socket.recv(self._read_buffer)
                        if data == b'':
                            self._connect = False
                            continue
                        if self._read_handler:
                            self._read_handler(data)
                        else:
                            self._logger.debug(f"Received: {repr(data)}")
                    except ConnectionResetError:
                        continue
            except OSError as e:
                self._logger.error("Receive Data Error")
