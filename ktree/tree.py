import abc
import typing

from ktree.libs import SupportNumber


class ClusterInterface(abc.ABC):
    @abc.abstractmethod
    def clear(self): ...

    @abc.abstractmethod
    def append(self, node: typing.List[SupportNumber]): ...

    @property
    @abc.abstractmethod
    def data(self): ...

    @property
    @abc.abstractmethod
    def axis(self): ...

    @abc.abstractmethod
    def __len__(self): ...

    @abc.abstractmethod
    def __hash__(self): ...

    @abc.abstractmethod
    def __iter__(self): ...

    @abc.abstractmethod
    def __repr__(self): ...


class TreeContainerInterface(abc.ABC):
    @abc.abstractmethod
    def insert(self, data: typing.List[SupportNumber]): ...

    @abc.abstractmethod
    def sort(self) -> typing.List[ClusterInterface]: ...

    @abc.abstractmethod
    def clear(self): ...

    @abc.abstractmethod
    def __iter__(self) -> typing.List[ClusterInterface]: ...
