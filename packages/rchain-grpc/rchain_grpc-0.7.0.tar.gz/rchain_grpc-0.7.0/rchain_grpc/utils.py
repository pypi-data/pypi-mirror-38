import functools
import json
from contextlib import AbstractContextManager
from typing import Any, Callable, Generic, List, Type, TypeVar

from grpc import Channel, insecure_channel

from .exceptions import ConnectionClosedException

gRPCStub = TypeVar('gRPCStub')


class Connection(AbstractContextManager, Generic[gRPCStub]):
    """proxy class from stub from grpc. Support `close` method
    and can be usee as context manager"""

    def __init__(self, channel: Channel, stub: gRPCStub) -> None:
        # NOTE: using super to avoid recursion
        super().__setattr__('connected', True)
        super().__setattr__('_channel', channel)
        super().__setattr__('_stub', stub)

    def close(self) -> None:
        self._channel.close()
        del self._channel
        del self._stub
        # NOTE: using super to avoid recursion
        super().__setattr__('connected', False)

    def __getattr__(self, key: str) -> Any:
        if not object.__getattribute__(self, 'connected'):
            raise ConnectionClosedException()
        return getattr(self._stub, key)

    def __setattr__(self, key: str, val: Any) -> None:
        if not object.__getattribute__(self, 'connected'):
            raise ConnectionClosedException()
        setattr(self._stub, key, val)

    def __exit__(self, *args, **kwargs) -> None:
        self.close()
        return super().__exit__(*args, **kwargs)


def create_connection(
    stub: Type[gRPCStub],
    channel_fn: Callable[[str], Channel] = insecure_channel,
    host: str = '127.0.0.1',
    port: int = 40401,
) -> Connection[gRPCStub]:
    """create new connection from `stub` generated by grpcio.
    Connection can be used as context manager"""

    channel = channel_fn(f'{host}:{port}')
    return Connection[stub](channel, stub(channel))


def create_connection_builder(stub: Type[Connection]) -> Callable[..., Connection]:
    """factory for cinnection functions created from `stub` generated by grpcio"""

    return functools.partial(create_connection, stub=stub)


def is_equal(d1: dict, d2: dict) -> bool:
    kwargs = {'sort_keys': True, 'indent': 0}
    return json.dumps(d1, **kwargs) == json.dumps(d2, **kwargs)


def register_many(dispatch: Callable[..., Any], types: List[Any]) -> Callable[..., Any]:
    """register many types to one handler from `functools.singledispatch`"""

    def decorator(fn):
        for t in types:
            fn = dispatch.register(t)(fn)
        return fn

    return decorator
