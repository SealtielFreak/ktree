import abc
import typing

T = typing.TypeVar('T')


class ClusterInterface(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def clear(self): ...

    @abc.abstractmethod
    def append(self, node: T): ...

    @property
    @abc.abstractmethod
    def data(self): ...

    @property
    @abc.abstractmethod
    def shape(self): ...

    @abc.abstractmethod
    def __len__(self): ...

    @abc.abstractmethod
    def __hash__(self): ...

    @abc.abstractmethod
    def __iter__(self): ...

    @abc.abstractmethod
    def __repr__(self): ...


class TreeContainerInterface(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def insert(self, data: T): ...

    @abc.abstractmethod
    def sort(self) -> typing.List[ClusterInterface]: ...

    @abc.abstractmethod
    def clear(self): ...

    @abc.abstractmethod
    def __iter__(self) -> typing.List[ClusterInterface]: ...
