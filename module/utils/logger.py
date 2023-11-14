from inspect import currentframe, getframeinfo
from os import mkdir, remove
from os.path import exists
from threading import Event, Thread
from threading import current_thread
from time import localtime, sleep, strftime
from typing import IO, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from module.enums.logger.log_level import LogLevel
from module.enums.logger.log_type import LogType


class Logger:
    _log_path: str = "./logs/"
    _compress_file: bool = False
    _log_level: LogLevel = LogLevel.INFO
    _log_file_name: str
    _log_file: IO
    _log_name: str
    _timer: Optional[Event] = None
    _prefix_name: str = ""
    _log_func = None

    def __init__(self, log_name: str = "Logger", log_path: Optional[str] = None, compress_file: bool = False,
                 log_level: Optional[LogLevel] = None, prefix_name: str = None, log_func=None) -> None:
        self._log_name = log_name
        if log_path is not None:
            self._log_path = log_path if log_path.endswith("/") else f"{log_path}/"
        if log_level is not None:
            self._log_level = log_level
        if prefix_name is not None:
            self._prefix_name = prefix_name
        else:
            self._prefix_name = log_name
        self._compress_file = compress_file
        if log_func is not None:
            self._log_func = log_func
        if not exists(self._log_path):
            mkdir(self._log_path)
        self._log_file_name = f"{self._prefix_name}" \
                              f"{'' if self._prefix_name == '' else '_'}" \
                              f"{self._log_level.name.lower()}_" \
                              f"{self.get_now_time()}.log"
        self._log_file = open(self._log_path + self._log_file_name, "a+", encoding="UTF-8")
        self._timer = Event()
        self.debug("Timer start")
        Thread(target=self._time_handler, name="Timer", args=(self._timer,), daemon=True).start()

    def __del__(self) -> None:
        self.debug("Exit logger")
        self._log_file.close()
        self.stop_timer()

    def __repr__(self) -> str:
        return (f"{'-' * 30}\n"
                f"Log Save Path: {self._log_path}\n"
                f"Log File Name: {self._log_file_name}\n"
                f"Log Level: {self._log_level.name}\n"
                f"{'-' * 30}")

    def stop_timer(self) -> None:
        self._timer.set()

    def _time_handler(self, event: Event) -> None:
        while True:
            temp = localtime()
            if temp.tm_hour == 0 and temp.tm_min == 0 and temp.tm_sec == 0:
                if self._compress_file:
                    self.debug("Compress File")
                    zip_file = ZipFile(f"{self._log_path}{strftime('%Y-%m-%dT%H-%M-%S', temp)}.zip", "w")
                    zip_file.write(f"{self._log_path}{self._log_file_name}", compress_type=ZIP_DEFLATED)
                    zip_file.close()
                    remove(f"{self._log_path}{self._log_file_name}")
                self._log_file_name = f"{self._prefix_name}" \
                                      f"{'' if self._prefix_name == '' else '_'}" \
                                      f"{self._log_level.name.lower()}_" \
                                      f"{self.get_now_time()}.log"
                self._log_file.close()
                self._log_file = open(self._log_path + self._log_file_name, "a+", encoding="UTF-8")
            if event.is_set():
                self.debug("Exit Timer")
                break
            sleep(1)

    @staticmethod
    def get_now_time(time: bool = False) -> str:
        if time:
            return strftime("%H:%M:%S", localtime())
        return strftime("%Y-%m-%d", localtime())

    def debug(self, msg: str, from_target: Optional[str] = None) -> None:
        if LogLevel.DEBUG.value >= self._log_level.value:
            self._log(LogType.DEBUG, from_target, msg, getframeinfo(currentframe().f_back))

    def info(self, msg: str, from_target: Optional[str] = None) -> None:
        if LogLevel.INFO.value >= self._log_level.value:
            self._log(LogType.INFO, from_target, msg, getframeinfo(currentframe().f_back))

    def warn(self, msg: str, from_target: Optional[str] = None) -> None:
        if LogLevel.WARN.value >= self._log_level.value:
            self._log(LogType.WARN, from_target, msg, getframeinfo(currentframe().f_back))

    def error(self, msg: str, from_target: Optional[str] = None) -> None:
        if LogLevel.ERROR.value >= self._log_level.value:
            self._log(LogType.ERROR, from_target, msg, getframeinfo(currentframe().f_back))

    def _log(self, log_type: LogType, from_target: Optional[str], msg: str, call_fun: tuple) -> None:
        time = self.get_now_time(True)
        msg = msg.format(time=time)
        file_name = call_fun[0].split('\\')[-1]
        output = f"[{time}] " \
                 f"[{log_type.value}] " \
                 f"[{current_thread().name}/{file_name}:{call_fun[2]}:{call_fun[1]}] " \
                 f"{self._log_name if from_target is None else from_target}: {msg}\n"
        print(output, end="")
        if self._log_func is not None:
            self._log_func(msg + "\n")
        self._log_file.writelines(output)
        self._log_file.flush()
