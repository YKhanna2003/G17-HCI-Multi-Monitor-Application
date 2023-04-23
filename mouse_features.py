version = '0.7.1'

import time as _time

import platform as _platform
if _platform.system() == 'Windows':
    from. import _winmouse as _os_mouse
elif _platform.system() == 'Linux':
    from. import _nixmouse as _os_mouse
elif _platform.system() == 'Darwin':
    from. import _darwinmouse as _os_mouse
else:
    raise OSError("Unsupported platform '{}'".format(_platform.system()))

from ._mouse_event import ButtonEvent, MoveEvent, WheelEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN, DOUBLE
from ._generic import GenericListener as _GenericListener

_pressed_events = set()
class _MouseListener(_GenericListener):
    def init(self):
        _os_mouse.init()
    def pre_process_event(self, event):
        if isinstance(event, ButtonEvent):
            if event.event_type in (UP, DOUBLE):
                _pressed_events.discard(event.button)
            else:
                _pressed_events.add(event.button)
        return True

    def listen(self):
        _os_mouse.listen(self.queue)

_listener = _MouseListener()

def is_pressed(button=LEFT):
    _listener.start_if_necessary()
    return button in _pressed_events

def press(button=LEFT):
    _os_mouse.press(button)

def release(button=LEFT):
    _os_mouse.release(button)

def click(button=LEFT):
    _os_mouse.press(button)
    _os_mouse.release(button)

def double_click(button=LEFT):
    click(button)
    click(button)

def right_click():
    click(RIGHT)

def wheel(delta=1):
    _os_mouse.wheel(delta)

def move(x, y, absolute=True, duration=0, steps_per_second=120.0):
    x = int(x)
    y = int(y)

    position_x, position_y = get_position()

    if not absolute:
        x = position_x + x
        y = position_y + y

    if duration:
        start_x = position_x
        start_y = position_y
        dx = x - start_x
        dy = y - start_y

        if dx == 0 and dy == 0:
            _time.sleep(duration)
        else:
            steps = max(1.0, float(int(duration * float(steps_per_second))))
            for i in range(int(steps)+1):
                move(start_x + dx*i/steps, start_y + dy*i/steps)
                _time.sleep(duration/steps)
    else:
        _os_mouse.move_to(x, y)

def drag(start_x, start_y, end_x, end_y, absolute=True, duration=0):
    if is_pressed():
        release()
    move(start_x, start_y, absolute, 0)
    press()
    move(end_x, end_y, absolute, duration)
    release()

def on_button(callback, args=(), buttons=(LEFT, MIDDLE, RIGHT, X, X2), types=(UP, DOWN, DOUBLE)):
    if not isinstance(buttons, (tuple, list)):
        buttons = (buttons,)
    if not isinstance(types, (tuple, list)):
        types = (types,)

    def handler(event):
        if isinstance(event, ButtonEvent):
            if event.event_type in types and event.button in buttons:
                callback(*args)
    _listener.add_handler(handler)
    return handler

def on_pressed(callback, args=()):
    return on_button(callback, args, [LEFT], [DOWN])

def on_click(callback, args=()):
    return on_button(callback, args, [LEFT], [UP])

def on_double_click(callback, args=()):
    return on_button(callback, args, [LEFT], [DOUBLE])

def on_middle_double_click(callback, args=()):
    return on_button(callback, args, [MIDDLE], [DOUBLE])



def on_right_click(callback, args=()):
    return on_button(callback, args, [RIGHT], [UP])

def on_middle_click(callback, args=()):
    return on_button(callback, args, [MIDDLE], [UP])

def wait(button=LEFT, target_types=(UP, DOWN, DOUBLE)):
    from threading import Lock
    lock = Lock()
    lock.acquire()
    handler = on_button(lock.release, (), [button], target_types)
    lock.acquire()
    _listener.remove_handler(handler)

def get_position():
    return _os_mouse.get_position()

def hook(callback):
    _listener.add_handler(callback)
    return callback

def unhook(callback):
    _listener.remove_handler(callback)

def unhook_all():
    del _listener.handlers[:]

def record(button=RIGHT, target_types=(DOWN,)):
    recorded = []
    hook(recorded.append)
    wait(button=button, target_types=target_types)
    unhook(recorded.append)
    return recorded

def play(events, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
    last_time = None
    for event in events:
        if speed_factor > 0 and last_time is not None:
            _time.sleep((event.time - last_time) / speed_factor)
        last_time = event.time

        if isinstance(event, ButtonEvent) and include_clicks:
            if event.event_type == UP:
                _os_mouse.release(event.button)
            else:
                _os_mouse.press(event.button)
        elif isinstance(event, MoveEvent) and include_moves:
            _os_mouse.move_to(event.x, event.y)
        elif isinstance(event, WheelEvent) and include_wheel:
            _os_mouse.wheel(event.delta)

replay = play
hold = press

if __name__ == '__main__':
    print('Recording... Double click to stop and replay.')
    play(record())