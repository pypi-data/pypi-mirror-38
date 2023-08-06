from typing import NoReturn


class UdpOptions:
    def __init__(self,
                 read_buffer_size:int=None,
                 send_buffer_size:int=None,
                 sp_rcvbuf:int=None,
                 sp_sndbuf:int=None,
                 loop:bool=None,
                 ttl:int=None,
                 timestampns:bool=None,
                 pktinfo:bool=None,
                 **kwargs) -> NoReturn: ...

    read_buffer_size = ... # type: int
    send_buffer_size = ... # type: int
    sp_rcvbuf = ... # type: int
    sp_sndbuf = ... # type: int
    loop = ... # type: bool
    ttl = ... # type: bool
    timestampns = ... # type: bool
    pktinfo = ... # type: bool


class TcpOptions:
    def __init__(self,
                 read_buffer_size:int=None,
                 send_buffer_size:int=None,
                 sp_rcvbuf:int=None,
                 sp_sndbuf:int=None,
                 listen_backlog:int=None,
                 no_delay:bool=None,
                 quick_ack:bool=None,
                 **kwargs) -> NoReturn: ...

    read_buffer_size = ... # type: int
    send_buffer_size = ... # type: int
    sp_rcvbuf = ... # type: int
    sp_sndbuf = ... # type: int
    listen_backlog = ... # type: int
    no_delay = ... # type: bool
    quick_ack = ... # type: bool