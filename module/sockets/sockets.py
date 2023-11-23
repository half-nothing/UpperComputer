from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from re import Pattern, compile
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM, socket, IPPROTO_TCP, IPPROTO_UDP
from threading import Event
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
    _socket_thread_pool: ThreadPoolExecutor = ThreadPoolExecutor(thread_name_prefix="SocketThreadPool")
    _socket: Optional[socket] = None
    _clients: Optional[set[socket]] = None
    _connect: bool = False
    _net_type: IPProtocol
    _mode: SocketMode
    _connect_type: ConnectType
    _local_addr: tuple[str, int]
    _remote_addr: tuple[str, int]
    _read_buffer: int
    _read_handler = None
    _broadcast: bool = False
    _logger: Logger
    _thread_stop: Event = Event()

    def __init__(self, net_type: IPProtocol, connect_protocol: ConnectType, mode: SocketMode,
                 local_host: Optional[str] = None, local_port: int = 8888, remote_host: Optional[str] = None,
                 remote_port: Optional[int] = 8888, read_buffer: int = 1024, read_handler=None, bind: bool = False):
        if net_type not in self.IPProtocol:
            raise Exception("IP protocol error")
        if connect_protocol not in self.ConnectType:
            raise Exception("Connection protocol error")
        if not remote_host and mode == Sockets.SocketMode.Client:
            raise Exception("Client mode need a valid ip address")
        if not local_host:
            local_host = "0.0.0.0" if net_type == self.IPProtocol.IPV4 else "::"
        self._local_addr = (local_host, local_port)
        self._remote_addr = (remote_host, remote_port)
        self._read_buffer, self._read_handler, self._mode = read_buffer, read_handler, mode
        self._net_type, self._connect_type = net_type, connect_protocol
        self._socket = socket(self._net_type.value, self._connect_type.value[1], self._connect_type.value[2])
        if bind:
            self._socket.bind(self._local_addr)
        self._logger = Logger(f"Sockets_{self._local_addr[0]}_{self._connect_type.value[0]}")
        self._thread_stop.clear()

    def __del__(self):
        self.clear()

    def clear(self):
        self._thread_stop.set()
        self.disconnect()
        if self._clients:
            for s in self._clients:
                s.shutdown(0)
                s.close()
        self._logger.clear()

    def __repr__(self):
        res = f"{'-' * 30}\n"
        res += f"Socket Mode: {self._mode.value}\n"
        if self.is_client and self.is_tcp:
            res += f"Connect Status: {self._connect}\n"
        res += f"Connect Protocol: {self._connect_type.value[0]}\n"
        res += f"IP Protocol: {'IPV4' if self.ipv4 else 'IPV6'}\n"
        if self.is_server:
            if self._broadcast:
                res += f"{'-' * 15}\n"
                res += f"Broadcast: True\n"
                res += f"Broadcast Port: {self._local_addr[1]}\n"
                res += f"{'-' * 15}\n"
            res += f"Listen Address: {self.local_address}\n"
        else:
            res += f"Local Address: {self.local_address}\n"
            res += f"Remote Address: {self.remote_address}\n"
        if self.is_server and self.is_tcp:
            res += f"Connect Clients: {len(self._clients)}\n"
            res += "Connect Client: %s\n" % " ".join(self._get_address(addr.getsockname()) for addr in self._clients)
        res += f"{'-' * 30}"
        return res

    @staticmethod
    def decode_data(data: Union[str, bytes], encoding: Optional[str] = None) -> bytes:
        if isinstance(data, bytes):
            return data
        if encoding:
            return bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode(encoding=encoding)))
        else:
            return bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode()))

    def send_data(self, data: Union[str, bytes], encoding: Optional[str] = None):
        if self.is_tcp and not self._connect:
            self._logger.error("The socket is not connected")
            return
        self._socket.send(self.decode_data(data, encoding))

    def send_data_to(self, data: Union[str, bytes], host: Optional[str] = None, port: Optional[int] = None,
                     encoding: Optional[str] = None):
        if self.is_udp and not self._connect:
            self._socket.sendto(self.decode_data(data, encoding),
                                (host if host else self._remote_addr[0], port if port else self._remote_addr[1]))

    def connect(self, host: Optional[str] = None, port: Optional[int] = None):
        if self._connect or self._broadcast:
            return
        try:
            self._socket.connect((host if host else self._remote_addr[0], port if port else self._remote_addr[1]))
            self._connect = True
        except ConnectionError:
            self._logger.error(f"Fail to connect {self.remote_address}")
            self._connect = False

    def disconnect(self):
        if self.is_udp:
            self._socket.close()
            return
        if not self._connect:
            return
        self._socket.shutdown(0)
        self._socket.close()

    def _recv_data(self):
        while True:
            if self._thread_stop.is_set():
                break
            try:
                if self.is_udp:
                    try:
                        data, addr = self._socket.recvfrom(self._read_buffer)
                        if self._read_handler:
                            self._read_handler(data, addr)
                        else:
                            self._logger.info(f"Received: {repr(data)}, from {self._get_address(addr)}")
                    except ConnectionResetError:
                        continue
                else:
                    try:
                        if not self._connect:
                            continue
                        data = self._socket.recv(self._read_buffer)
                        if data == b'':
                            self._connect = False
                            self._logger.info(f"Disconnect from {self.remote_address}")
                            continue
                        if self._read_handler:
                            self._read_handler(data)
                        else:
                            self._logger.info(f"Received: {repr(data)}")
                    except ConnectionResetError:
                        continue
            except OSError as e:
                continue

    def _get_address(self, addr: tuple[str, int]) -> str:
        return ("%s:%d" if self.ipv4 else '[%s]:%d') % (addr[0], addr[1])

    @property
    def ipv4(self):
        return self._net_type == Sockets.IPProtocol.IPV4

    @property
    def remote_address(self):
        return self._get_address(self._remote_addr)

    @property
    def local_address(self):
        return self._get_address(self._local_addr)

    @property
    def thread_pool(self):
        return Sockets._socket_thread_pool

    @property
    def is_server(self):
        return self._mode == Sockets.SocketMode.Server

    @property
    def is_client(self):
        return self._mode == Sockets.SocketMode.Client

    @property
    def is_tcp(self):
        return self._connect_type == Sockets.ConnectType.TCP

    @property
    def is_udp(self):
        return self._connect_type == Sockets.ConnectType.UDP
