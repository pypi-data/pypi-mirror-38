from datetime import timedelta
from typing import Callable, NoReturn, Optional, Union


class RendezvousError:
    where = ... # type: str


class Dispatcher:
    def __init__(self,
                 error_callback: Callable[[Exception], NoReturn],
                 parent: Dispatcher = None) -> NoReturn : ...
    def dispatch(self,
                 timeout: Optional[Union[float, timedelta]] = None) -> bool : ...


class Loop:
    def __init__(self, dispatcher: Dispatcher) -> NoReturn: ...

    def run_forever(self) -> NoReturn: ...
    def interrupt(self) -> NoReturn: ...
    def interrupt_on(self, signo: int) -> NoReturn: ...

