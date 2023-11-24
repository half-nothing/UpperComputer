from enum import Enum
from typing import Optional, Union

from serial import EIGHTBITS, PARITY_EVEN, PARITY_NONE, PARITY_ODD, SEVENBITS, SIXBITS, STOPBITS_ONE, STOPBITS_TWO
from serial import Serial, SerialException
from serial.tools import list_ports

from module.utils.logger import Logger


class SerialManager:
    _logger: Optional[Logger] = None
    _serial: Optional[Serial] = None
    port: str
    rate: int

    class ByteSize(Enum):
        EightBits = EIGHTBITS
        SevenBits = SEVENBITS
        SixBits = SIXBITS

    class Parity(Enum):
        ParityNone = PARITY_NONE
        ParityEven = PARITY_EVEN
        ParityOdd = PARITY_ODD

    class StopBits(Enum):
        OneBit = STOPBITS_ONE
        TwoBit = STOPBITS_TWO

    def __init__(self, port: str, rate: int = 9600, byte_size: ByteSize = ByteSize.EightBits,
                 parity: Parity = Parity.ParityNone, stop_bits: StopBits = StopBits.OneBit,
                 xon_xoff: bool = False, rts_cts: bool = False, dsr_dtr: bool = False,
                 logger: Optional[Logger] = None) -> None:
        self.port = port.lower()
        self.rate = rate
        self._serial = Serial(port, rate, byte_size.value, parity.value, stop_bits.value, xonxoff=xon_xoff,
                              rtscts=rts_cts,
                              dsrdtr=dsr_dtr)
        self._logger = Logger("SerialLogger", prefix_name=f"Serial_{self.port}") if logger is None else logger
        if self.open:
            self._logger.info(f"{self.port}打开成功, 波特率:{self.rate}", f"Serial-{self.port}")

    def __del__(self):
        self.clear()

    def clear(self):
        self._logger.clear()

    def close(self) -> bool:
        if not self.open:
            return True
        try:
            self._serial.close()
        except SerialException as _:
            self._logger.error(f"串口{self.port}关闭失败", f"Serial-{self.port}")
            return False
        else:
            self._logger.info(f"串口{self.port}关闭成功", f"Serial-{self.port}")
            return True

    def read(self, size: int) -> bytes:
        return self._serial.read(size)

    def read_all(self) -> bytes:
        return self._serial.read(self.waiting)

    def send(self, data: Union[str, bytes], encoding: Optional[str] = None) -> bool:
        if not self.open:
            self._logger.error(f"串口{self.port}未打开,无法发送数据", f"Serial-{self.port}")
            return False
        if isinstance(data, str):
            if encoding:
                data = bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode(encoding=encoding)))
            else:
                data = bytes.fromhex(''.join(fr"{c:02x}" for c in data.encode()))
        self._serial.write(data)
        self._logger.info(f"串口{self.port}发送成功: {data}", f"Serial-{self.port}")
        return True

    def __repr__(self) -> str:
        return (f"{'-' * 30}\n"
                f"Serial Port: {self.port}\n"
                f"Serial Rate: {self.rate}\n"
                f"Serial ByteSize: {self._serial.bytesize}\n"
                f"Serial Parity: {self._serial.parity}\n"
                f"Serial XonXoff: {self._serial.xonxoff}\n"
                f"Serial RtsCts: {self._serial.rtscts}\n"
                f"Serial DsrDtr: {self._serial.dsrdtr}\n"
                f"{self._logger.__repr__()}")

    @property
    def waiting(self) -> Optional[int]:
        try:
            return self._serial.in_waiting
        except SerialException:
            return None

    @property
    def open(self) -> bool:
        return self._serial.is_open

    @staticmethod
    def get_serials() -> list:
        res = []
        port_list = list(list_ports.comports())
        for i in port_list:
            res.append(list(i)[0])
        return res
