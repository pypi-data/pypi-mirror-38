from gui import GUI
from gamepad_handler import Gamepad
from websocket_client import WebsocketClient

from PyQt5.QtWidgets import QApplication
from threading import Thread
from enum import Enum, IntEnum, unique
import sys
import struct
import logging

logging.basicConfig(style='{', format=r'{levelname:7s} - {module}:{lineno:<3d} - {message}', level=logging.INFO)


class GamepadState(Enum):
    DETACHED = -1,
    DISABLED = 0,
    ENABLED = 1,


@unique
class WifiCmds(IntEnum):
    MOTOR_LEFT_SPEED = 0x0A,
    MOTOR_RIGHT_SPEED = 0x0B,
    PROP_LEFT_SPEED = 0x0C,
    PROP_RIGHT_SPEED = 0x0D,
    STOP_ALL = 0x10,


SERVER_PORT = 5005


class WifiLinkClient:
    def __init__(self):
        self._gui = self._init_gui()
        self._gamepad: Gamepad = None

        self._websocket: WebsocketClient = None

        self._gamepad_state = GamepadState.DETACHED

        # If true, joysticks control propellers instead of drive motors
        self._props_on_joysticks = False

    def _init_gui(self):
        gui = GUI()

        # Event Handlers ####

        def on_clicked_btn_gamepad():
            if self._gamepad_state == GamepadState.DETACHED:
                # Attach gamepad
                try:
                    gui.btn_gamepad.setEnabled(False)
                    self._gamepad = self._init_gamepad()

                except IOError:
                    logging.warning('No gamepad found')
                    self._gui.btn_gamepad.setEnabled(True)
                else:
                    # Update state, if gamepad was attached successfully
                    self._gui.btn_gamepad.setEnabled(True)
                    self._gui.btn_gamepad.setText('ENABLE\nGamepad')
                    self._gui.btn_gamepad.setStyleSheet('background-color: #81C784')
                    self._gamepad_state = GamepadState.DISABLED

            elif self._gamepad_state == GamepadState.DISABLED:
                # Enable WiFi control

                # Update state
                self._gui.btn_gamepad.setText('DISABLE\nGamepad')
                self._gui.btn_gamepad.setStyleSheet('background-color: #E57373')
                self._gamepad_state = GamepadState.ENABLED
            else:
                # Disable WiFi control

                # Update state
                self._gui.btn_gamepad.setText('ENABLE\nGamepad')
                self._gui.btn_gamepad.setStyleSheet('background-color: #81C784')
                self._gamepad_state = GamepadState.DISABLED

        gui.btn_gamepad.clicked.connect(on_clicked_btn_gamepad)

        def on_clicked_btn_wifi_connect():
            global sock
            gui.btn_wifi_connect.setText('Connecting...')
            gui.btn_wifi_connect.setEnabled(False)
            gui.txt_ip.setEnabled(False)

            addr = gui.txt_ip.text()
            logging.info(f'Connecting to {addr}:{SERVER_PORT}...')

            try:
                self._websocket = WebsocketClient(addr, SERVER_PORT)
            except Exception as ex:
                logging.warning(f'WiFi connection failed: {ex}')
                self._gui.btn_wifi_connect.setText('Connect')
                self._gui.btn_wifi_connect.setEnabled(True)
                self._gui.txt_ip.setEnabled(True)
            else:
                self._gui.btn_wifi_connect.setText('Connected')
                logging.info('Connected!')

        # Connect to thread, to avoid blocking gui thread
        gui.btn_wifi_connect.clicked.connect(
            lambda: Thread(target=on_clicked_btn_wifi_connect, daemon=True).start())

        gui.show()
        return gui

    def _init_gamepad(self):
        gamepad = Gamepad()

        # Event Handlers ####

        def on_btn_start_select(state):
            """ When start or select is pressed, click the gamepad enabled toggle button """
            if state:
                self._gui.btn_gamepad.click()
        gamepad.on_btn_start = on_btn_start_select
        gamepad.on_btn_select = on_btn_start_select

        def on_btn_a(state):
            if self._gamepad_state == GamepadState.ENABLED:
                print(f'A: {bool(state)}')
        gamepad.on_btn_a = on_btn_a

        def on_btn_x(state):
            self._gui.close()
        gamepad.on_btn_x = on_btn_x

        def on_btn_y(state):
            if self._gamepad_state == GamepadState.ENABLED and state:
                self._props_on_joysticks = not self._props_on_joysticks
                print('Joysticks: {}'.format('Propellers' if self._props_on_joysticks else 'Drive motors'))
        gamepad.on_btn_y = on_btn_y

        def joy_to_speed_cmd(joy_val: int):
            return struct.pack('!h', joy_val // 128)

        def on_joystick_any():
            if self._gamepad_state == GamepadState.ENABLED:
                print(f'{gamepad.left_joy_y // 128: 7d}\t{gamepad.right_joy_y // 128: 7d}')
                self._websocket.send_cmd(b'\x0A', joy_to_speed_cmd(self._gamepad.left_joy_y))
                self._websocket.send_cmd(b'\x0B', joy_to_speed_cmd(self._gamepad.right_joy_y))
        gamepad.on_joystick_any = on_joystick_any

        def on_trigger_any():
            if self._gamepad_state == GamepadState.ENABLED:
                print(f'{gamepad.left_trigger: 7d}\t{gamepad.right_trigger: 7d}')
        gamepad.on_trigger_any = on_trigger_any

        gamepad.start()
        return gamepad

    def shutdown(self):
        logging.info('Shutting down...')
        if self._websocket is not None:
            self._websocket.close()


def main():
    app = QApplication(sys.argv)
    client = WifiLinkClient()
    app.exec_()

    client.shutdown()


if __name__ == '__main__':
    main()
