
from typing import Protocol


class Component(Protocol):
    def update(self, delta_time: float):
        ...

    def render(self):
        ...

    def key_callback(self, key: int, action: int):
        ...
