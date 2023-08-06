import socket
import time
import select
import logging


class SockerServer:
    def __init__(self, iface: str, port: int):
        self.sock_ = socket.socket()
        self.sock_.bind((iface, port))
        self.sock_.listen(5)

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.safe_close()

    def safe_close(self):
        try:
            if self.sock_:
                self.sock_.shutdown(1)
                self.sock_.close()
                self.sock_ = None
        except Exception as ex:
            pass


class TcpChannel:
    nb_connect_attempts = 3

    def __init__(self, addr: str, port: int):
        assert isinstance(addr, str), addr
        assert isinstance(port, int), port

        self.log = logging.getLogger('tcp_channel')

        self.log.debug('Try connect to %s:%s ...', addr, port)
        self.sock_ = None

        for i in range(self.nb_connect_attempts):
            try:
                self.sock_ = socket.create_connection((addr, port), timeout=5.0)
                break
            except:
                self.sock_ = None
                self.log.info('Failed connect to %s:%s attempt %s/%s', addr, port, i + 1, self.nb_connect_attempts)
                time.sleep(3.0)

        if self.sock_ is None:
            raise Exception("Failed connect to {}:{}".format(addr, port))

        self.log.debug('Connected to %s:%s', addr, port)

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.safe_close()

    def safe_close(self):
        try:
            if self.sock_:
                self.sock_.shutdown(1)
                self.sock_.close()
                self.sock_ = None
        except Exception as ex:
            self.log.debug('Error closing socket: %s', ex)

    def write_all(self, d: (str, bytes, bytearray)) -> None:
        assert isinstance(d, (str, bytes, bytearray)), d

        if self.sock_:
            self.log.debug('S> %s', d)
            self.sock_.sendall(d.encode('utf-8') if isinstance(d, str) else d)

    def raw_read_bytes(self, timeout_sec: float = 5.0) -> bytes:
        if self.sock_:
            fd_read, fd_write, fd_err = select.select([self.sock_], [], [], timeout_sec)
            if self.sock_ in fd_read:
                data = self.sock_.recv(1024)
                if data:
                    self.log.debug('R< %s', data)
                    return data
                else:
                    raise Exception('Socket closed while reading')
            else:
                return b''
        else:
            raise Exception('Socket is closed - cant read')

    def raw_read_str(self, timeout_sec: float = 5.0):
        return self.raw_read_bytes(timeout_sec).decode('utf-8')


