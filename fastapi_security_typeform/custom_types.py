from typing import (
    Callable,
    Union,
)

HashMethodType = Callable[[bytes, Union[bytes, bytearray]], str]
