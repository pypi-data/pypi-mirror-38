import json
import json.decoder
import time

from .tcp_channel import TcpChannel


DEFAULT_VOLCANO_TEST_HOST = 'volcano'
DEFAULT_VOLCANO_PORT = 8091


class VolcanoClient:
    def __init__(self, host: str = DEFAULT_VOLCANO_TEST_HOST, port: int = DEFAULT_VOLCANO_PORT):
        self.ch_ = TcpChannel(host, port)
        self.rcv_str_ = ''
        self.tags_ = None  # { tag_name: (v,q), ... }

    def __enter__(self):
        return self

    def safe_close(self):
        self.ch_.safe_close()

    def __exit__(self, t, v, tb):
        self.safe_close()

    def channel(self) -> TcpChannel:
        return self.ch_

    def set_tag(self, name: str, value, quality: int = 0) -> None:
        assert isinstance(name, str), name
        assert isinstance(quality, int), quality

        self.write_msg({'c': 'set', 'tag': name, 'v': value, 'q': quality})

    def write_msg(self, msg: dict) -> None:
        assert isinstance(msg, dict), msg

        self.ch_.write_all(json.dumps(msg) + '\n')

    def try_read_line(self, timeout_sec: float = 5.0) -> (str, None):
        t1 = time.perf_counter()
        while True:
            pos = self.rcv_str_.find('\n')
            while pos != -1:
                rs = self.rcv_str_[:pos].strip()
                self.rcv_str_ = self.rcv_str_[pos + 1:]
                if rs:
                    return rs
                else:
                    pos = self.rcv_str_.find('\n')

            sec_passed = time.perf_counter() - t1
            sec_remain = timeout_sec - sec_passed
            if sec_remain <= 0:
                return None
            self.rcv_str_ += self.ch_.raw_read_str(sec_remain)

    def read_msg_n(self, timeout_sec: float = 5.0) -> (dict, None):
        rs = self.try_read_line(timeout_sec)
        return json.loads(rs) if rs else None

    def sub_all(self):
        self.write_msg({'c': 'sub', 'tag': '*', 'ref': 'name'})
        self.tags_ = {}

    # value = None  => value не проверяется
    # quality = 0   => качество ПРОВЕРЯЕТСЯ на 0
    # quality = None => качество не проверяется
    def wait_tag(self, name: str, value=None, quality: (int, None) = 0, timeout: float = 5.0) -> None:
        assert isinstance(name, str), name
        assert value is not None or quality is not None, "Value or quality should be specified"
        assert self.tags_ is not None, 'Before calling wait_tag you need to subscribe by calling sub_all()'

        t1 = time.perf_counter()
        while True:
            vq = self.tags_.get(name)
            if vq:
                v, q = vq
                if value is not None:
                    if isinstance(v, (int, float)):
                        value_ok = abs(value - v) <= 0.01 if isinstance(value, float) else value == v
                    else:
                        value_ok = False
                else:
                    value_ok = True

                quality_ok = True if quality is None else quality == q

                if value_ok and quality_ok:
                    return

            sec_passed = time.perf_counter() - t1
            sec_remain = timeout - sec_passed
            if sec_remain > 0.0:
                msg = self.read_msg_n(sec_remain)
                if msg and msg['c'] == 'upd':
                    self.tags_[msg['tag']] = (msg['v'], msg['q'])
            else:
                if vq is None:
                    if quality:
                        raise Exception('Error waiting {}={}<{}>: tag has never updated'.format(name, value, quality))
                    else:   # если None, значит, пофиг; если 0, значит GOOD, но в обоих случаях его нет смысла выводить
                        raise Exception('Error waiting {}={}: tag has never updated'.format(name, value))

                v, q = vq
                if value is not None and quality is not None:
                    raise Exception('Error waiting {}={}<{}>. Now {}={}<{}>'.format(name, value, quality, name, v, q))
                elif value is not None:
                    raise Exception('Error waiting {}={}. Now {}={}'.format(name, value, name, v))
                else:
                    raise Exception('Error waiting {} quality {}. Now {} quality is {}'.format(name, quality, name, q))
