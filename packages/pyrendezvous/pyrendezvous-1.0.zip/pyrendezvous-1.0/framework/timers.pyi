from datetime import timedelta
from typing import Callable, NoReturn
from .framework import Dispatcher, RendezvousError


class OneShotTimer:
    def __init__(self,
                 dispatcher: Dispatcher,
                 elapsed_callback: Callable[[OneShotTimer], NoReturn],
                 error_callback: Callable[[RendezvousError], NoReturn]) -> NoReturn: ...

    is_armed = ... # type: bool

    def schedule(self, interval: timedelta) -> NoReturn: ...
    def disarm(self) -> NoReturn: ...


class AutoReloadTimer:
    def __init__(self,
                 dispatcher: Dispatcher,
                 interval: timedelta,
                 elapsed_callback: Callable[[OneShotTimer], NoReturn],
                 error_callback: Callable[[RendezvousError], NoReturn]) -> NoReturn: ...

    is_armed = ... # type: bool

    def arm(self) -> NoReturn: ...
    def disarm(self) -> NoReturn: ...
