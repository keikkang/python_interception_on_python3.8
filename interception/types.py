from typing import Union
from typing_extensions import Literal  # Python 3.8에서 Literal을 사용하기 위함

MouseButton = Union[str, Literal["left", "right", "middle", "mouse4", "mouse5"]]