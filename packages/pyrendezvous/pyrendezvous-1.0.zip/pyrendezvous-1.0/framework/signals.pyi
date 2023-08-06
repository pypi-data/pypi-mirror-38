from typing import Callable, NoReturn
from .framework import Dispatcher


class SignalHandler:
    def __init__(self,
                 dispatcher: Dispatcher,
                 singno: int,
                 receive_callback: Callable[[int], NoReturn],
                 error_callback: Callable[[Exception], NoReturn] = None) -> NoReturn : ...