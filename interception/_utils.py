from typing import Union, Tuple, Optional
import functools
from threading import Thread
import win32api  # type: ignore


def normalize(x: Union[int, Tuple[int, int]], y: Optional[int] = None) -> Tuple[int, int]:
    """Normalizes an x, y position to allow passing them separately or as tuple."""
    if isinstance(x, tuple):
        if len(x) == 2:
            x, y = x
        elif len(x) == 4:
            x, y, *_ = x
        else:
            raise ValueError(f"Can't normalize tuple of length {len(x)}: {x}")
    else:
        if y is None:
            raise AssertionError("Y value must not be None")
        # 이 부분은 수정할 필요가 없으며, assert 대신에 if 문과 예외 처리를 사용하여 명시적으로 처리합니다.
    
    return int(x), int(y)


def to_interception_coordinate(x: int, y: int) -> Tuple[int, int]:
    """Scales a "normal" coordinate to the respective point in the interception
    coordinate system.

    The interception coordinate system covers all 16-bit unsigned integers,
    ranging from `0x0` to `0xFFFF (65535)`.

    To arrive at the formula, we first have to realize the following:
        - The maximum value in the 16-bit system is so `0xFFFF (~65535)`
        - The maximum value, depending on your monitor, would for example be `1920`
        - To calculate the factor, we can calculate `65535 / 1920 = ~34.13`.
        - Thus we found out, that `scaled x = factor * original x` and `factor = 0xFFFF / axis`

    So, to bring it to code:
    ```py
    xfactor = 0xFFFF / screen_width
    yfactor = 0xFFFF / screen_height
    ```

    Now, using that factor, we can calculate the position of our coordinate as such:
    ```py
    interception_x = round(xfactor * x)
    interception_y = round(yfactor * y)
    """

    def scale(dimension: int, point: int) -> int:
        return int((0xFFFF / dimension) * point) + 1

    screen = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    return scale(screen[0], x), scale(screen[1], y)


def get_cursor_pos() -> Tuple[int, int]:
    """Gets the current position of the cursor using `GetCursorPos`"""
    return win32api.GetCursorPos()


def threaded(name: str):
    """Threads a function, beware that it will lose its return values"""

    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            def run():
                func(*args, **kwargs)

            thread = Thread(target=run, name=name)
            thread.start()

        return inner

    return outer
