import time
from enum import unique, Enum
from multiprocessing import Process
from threading import Thread
from queue import Queue
from typing import Callable


@unique
class GamepadEvents(Enum):
    LEFT_JOYSTICK_X = 'ABS_X'
    LEFT_JOYSTICK_Y = 'ABS_Y'
    LEFT_JOYSTICK_BTN = 'BTN_THUMBL'
    RIGHT_JOYSTICK_X = 'ABS_RX'
    RIGHT_JOYSTICK_Y = 'ABS_RY'
    RIGHT_JOYSTICK_BTN = 'BTN_THUMBR'
    LEFT_TRIGGER = 'ABS_Z'
    RIGHT_TRIGGER = 'ABS_RZ'
    LEFT_SHOULDER = 'BTN_TL'
    RIGHT_SHOULDER = 'BTN_TR'
    DPAD_X = 'ABS_HAT0X'
    DPAD_Y = 'ABS_HAT0Y'
    BTN_START = 'BTN_START'
    BTN_SELECT = 'BTN_SELECT'
    BTN_A = 'BTN_SOUTH'
    BTN_B = 'BTN_EAST'
    BTN_X = 'BTN_WEST'
    BTN_Y = 'BTN_NORTH'


class Gamepad:
    def __init__(self, **kwargs):
        self._event_handlers = self._attach_event_handlers()

        # Gamepad handler process
        self._gamepad_queue = Queue()
        self._gamepad_process: Thread = ...
        self._thread: Thread = ...

        # How often to check the gamepad for state changes
        self._update_interval = 0.1

        # Dead zone for joysticks (0 - 32767)
        self.joy_dead_zone = 255
        # Exponent to apply to joystick output, to control sensitivity (0 < x < infinity), where 1 is neutral
        self.joy_exponent = 3.0

        # State variables for each control
        self.left_joy_x_raw = 0
        self.left_joy_y_raw = 0
        self.left_joy_btn = False

        self.right_joy_x_raw = 0
        self.right_joy_y_raw = 0
        self.right_joy_btn = False

        self.left_trigger = 0
        self.right_trigger = 0
        self.left_shoulder = False
        self.right_shoulder = False

        self.dpad_x = 0
        self.dpad_y = 0

        self.btn_start = False
        self.btn_select = False

        self.btn_a = False
        self.btn_b = False
        self.btn_x = False
        self.btn_y = False

        self.btn_dpad_left = False
        self.btn_dpad_right = False
        self.btn_dpad_up = False
        self.btn_dpad_down = False

        # User-provided callback functions
        def unassigned(state=1):
            pass

        self.on_trigger_left: Callable = unassigned
        self.on_trigger_right: Callable = unassigned
        self.on_trigger_any: Callable = unassigned
        self.on_shoulder_left: Callable = unassigned
        self.on_shoulder_right: Callable = unassigned
        self.on_joystick_any: Callable = unassigned

        self.on_btn_a: Callable = unassigned
        self.on_btn_b: Callable = unassigned
        self.on_btn_x: Callable = unassigned
        self.on_btn_y: Callable = unassigned
        self.on_btn_start: Callable = unassigned
        self.on_btn_select: Callable = unassigned
        self.on_btn_dpad_left: Callable = unassigned
        self.on_btn_dpad_right: Callable = unassigned
        self.on_btn_dpad_up: Callable = unassigned
        self.on_btn_dpad_down: Callable = unassigned
        self.on_btn_joy_left: Callable = unassigned
        self.on_btn_joy_right: Callable = unassigned
        self.on_btn_any: Callable = unassigned

    def start(self, update_interval=0.1):
        self._update_interval = update_interval

        # Start gamepad updater in separate thread
        self._gamepad_process = Thread(target=self._gamepad_loop,
                                       args=(self._gamepad_queue, self._update_interval))
        self._gamepad_process.daemon = True
        self._gamepad_process.start()
        self._gamepad_process.join(1.0)
        if not self._gamepad_process.is_alive():
            raise IOError('No gamepad found')

        # Start gamepad checker in separate thread
        self._thread = Thread(target=self._check_gamepad, daemon=True)
        self._thread.start()

    def _check_gamepad(self):
        while True:
            # Check for new events from the gamepad
            event_occured = False
            while not self._gamepad_queue.empty():
                event_code, event_state = self._gamepad_queue.get_nowait()

                if event_code != 'SYN_REPORT':  # Sync reports are just a keep-alive signal
                    event_occured = True
                    # Call handler function for the gamepad event
                    handler = self._event_handlers.get(GamepadEvents(event_code))
                    if handler:
                        handler(event_state)
            time.sleep(self._update_interval)

    def _attach_event_handlers(self):
        # Joystick

        def handle_left_joystick_x(state: int):
            self.left_joy_x_raw = state
            self.on_joystick_any()

        def handle_left_joystick_y(state: int):
            self.left_joy_y_raw = state
            self.on_joystick_any()

        def handle_left_joystick_btn(state: bool):
            self.left_joy_btn = state
            self.on_btn_joy_left(state)
            self.on_btn_any()

        def handle_right_joystick_x(state: int):
            self.right_joy_x_raw = state
            self.on_joystick_any()

        def handle_right_joystick_y(state: int):
            self.right_joy_y_raw = state
            self.on_joystick_any()

        def handle_right_joystick_btn(state: bool):
            self.right_joy_btn = state
            self.on_btn_joy_right(state)
            self.on_btn_any()

        # Triggers and Shoulder Buttons

        def handle_left_trigger(state: int):
            self.left_trigger = state
            self.on_trigger_left(state)
            self.on_trigger_any()
            self.on_btn_any()

        def handle_right_trigger(state: int):
            self.right_trigger = state
            self.on_trigger_right(state)
            self.on_trigger_any()
            self.on_btn_any()

        def handle_left_shoulder(state: bool):
            self.left_shoulder = state
            self.on_shoulder_left(state)

        def handle_right_shoulder(state: bool):
            self.right_shoulder = state
            self.on_shoulder_right(state)

        # D-Pad

        def handle_dpad_x(state: int):
            self.dpad_x = state

            prev_left = self.btn_dpad_left
            prev_right = self.btn_dpad_right

            self.btn_dpad_left = (state == -1)
            self.btn_dpad_right = (state == 1)

            # Handle button state changes
            if self.btn_dpad_left != prev_left:
                self.on_btn_dpad_left(self.btn_dpad_left)

            if self.btn_dpad_right != prev_right:
                self.on_btn_dpad_right(self.btn_dpad_right)

            self.on_btn_any()

        def handle_dpad_y(state: int):
            self.dpad_y = state

            prev_up = self.btn_dpad_up
            prev_down = self.btn_dpad_down

            self.btn_dpad_up = (state == 1)
            self.btn_dpad_down = (state == -1)

            # Handle button state changes
            if self.btn_dpad_up != prev_up:
                self.on_btn_dpad_up(self.btn_dpad_up)

            if self.btn_dpad_down != prev_down:
                self.on_btn_dpad_down(self.btn_dpad_down)

            self.on_btn_any()

        # Start and Select Buttons

        def handle_btn_start(state: bool):
            self.btn_start = state
            self.on_btn_start(state)
            self.on_btn_any()

        def handle_btn_select(state: bool):
            self.btn_select = state
            self.on_btn_select(state)
            self.on_btn_any()

        # ABXY Buttons

        def handle_btn_a(state: bool):
            self.btn_a = state
            self.on_btn_a(state)
            self.on_btn_any()

        def handle_btn_b(state: bool):
            self.btn_b = state
            self.on_btn_b(state)
            self.on_btn_any()

        def handle_btn_x(state: bool):
            self.btn_x = state
            self.on_btn_x(state)
            self.on_btn_any()

        def handle_btn_y(state: bool):
            self.btn_y = state
            self.on_btn_y(state)
            self.on_btn_any()

        # Build dictionary, so handlers can be referenced in a switch-case style
        handler_dict = {
            GamepadEvents.LEFT_JOYSTICK_X: handle_left_joystick_x,
            GamepadEvents.LEFT_JOYSTICK_Y: handle_left_joystick_y,
            GamepadEvents.LEFT_JOYSTICK_BTN: handle_left_joystick_btn,
            GamepadEvents.RIGHT_JOYSTICK_X: handle_right_joystick_x,
            GamepadEvents.RIGHT_JOYSTICK_Y: handle_right_joystick_y,
            GamepadEvents.RIGHT_JOYSTICK_BTN: handle_right_joystick_btn,
            GamepadEvents.LEFT_TRIGGER: handle_left_trigger,
            GamepadEvents.RIGHT_TRIGGER: handle_right_trigger,
            GamepadEvents.LEFT_SHOULDER: handle_left_shoulder,
            GamepadEvents.RIGHT_SHOULDER: handle_right_shoulder,
            GamepadEvents.DPAD_X: handle_dpad_x,
            GamepadEvents.DPAD_Y: handle_dpad_y,
            GamepadEvents.BTN_START: handle_btn_start,
            GamepadEvents.BTN_SELECT: handle_btn_select,
            GamepadEvents.BTN_A: handle_btn_a,
            GamepadEvents.BTN_B: handle_btn_b,
            GamepadEvents.BTN_X: handle_btn_x,
            GamepadEvents.BTN_Y: handle_btn_y,
        }
        return handler_dict

    @staticmethod
    def _gamepad_loop(event_queue: Queue, update_interval):
        """ Writes gamepad events (joystick and button state changes) to a queue for handling

         Meant to be called as a separate process

         :param event_queue: the blocking queue that gamepad events will be written to
         :raise IOError: if no gamepad is found
         """
        # Library to handle gamepad. Imported here, because it checks for connected gamepads on import
        import inputs

        try:
            gamepad = iter(inputs.devices.gamepads[0])
        except IndexError:
            # Error state is indicated by failure of process
            pass
        else:
            # Copy gamepad events to queue
            while True:
                for events in gamepad:
                    for event in events:
                        event_queue.put((event.code, event.state))
                time.sleep(update_interval)

    @property
    def left_joy_x(self):
        if abs(self.left_joy_x_raw) <= self.joy_dead_zone:
            return 0
        val = abs(self.left_joy_x_raw) / 32768.0
        sign = 1 if self.left_joy_x_raw > 0 else -1
        return int(32768 * val ** self.joy_exponent)

    @property
    def left_joy_y(self):
        if abs(self.left_joy_y_raw) <= self.joy_dead_zone:
            return 0
        val = abs(self.left_joy_y_raw) / 32768.0
        sign = 1 if self.left_joy_y_raw > 0 else -1
        return sign * int(32768 * val ** self.joy_exponent)

    @property
    def right_joy_x(self):
        if abs(self.right_joy_x_raw) <= self.joy_dead_zone:
            return 0
        val = abs(self.right_joy_x_raw) / 32768.0
        sign = 1 if self.right_joy_x_raw > 0 else -1
        return sign * int(32768 * val ** self.joy_exponent)

    @property
    def right_joy_y(self):
        if abs(self.right_joy_y_raw) <= self.joy_dead_zone:
            return 0
        val = abs(self.right_joy_y_raw) / 32768.0
        sign = 1 if self.right_joy_y_raw > 0 else -1
        return sign * int(32768 * val ** self.joy_exponent)
