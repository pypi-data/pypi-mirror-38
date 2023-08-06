import struct
import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class WebsocketClient:
    def __init__(self, addr: str, port: int, keep_alive_byte=b'\xFE', keep_alive_interval=0.5):
        # Initialize websocket
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.connect((addr, port))

        # Start keep-alive sender thread, if enabled
        if keep_alive_interval != -1:
            self._start_keep_alive_thread(keep_alive_byte, keep_alive_interval)

    def send_cmd(self, cmd: bytes, data=bytes()):
        """ Sends a command to the websocket server

         Command structure: [command byte][data length short][data 0][data 1]...

         :param cmd: command byte (0x00 - 0xFF) to send to server
         :param data: data bytes to send with command
         """
        if not (b'\x00' <= cmd <= b'\xFF'):
            raise ValueError('Command byte must be between 0x00 and 0xff, got {:#x}')

        packet = cmd + struct.pack('!H', len(data)) + data
        self._sock.sendall(packet)

    def close(self):
        self._sock.close()

    def _start_keep_alive_thread(self, keep_alive_byte: bytes, interval: float):
        """ Regularly sends a keep-alive packet to the server """

        def send_keep_alive():
            while True:
                self.send_cmd(keep_alive_byte)
                time.sleep(interval)
        Thread(target=send_keep_alive, daemon=True).start()
