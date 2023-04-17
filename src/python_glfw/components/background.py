import math

import moderngl


class Background:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.time = 0

    def key_callback(self, key: int, action: int):
        pass

    def update(self, delta_time: float):
        self.time += delta_time

    def render(self):
        self.ctx.clear(
            0,
            0,
            (math.sin(self.time) + 1.0) / 2,
            # (math.sin(time + 10) + 1.0) / 2,
            # (math.sin(time + 30) + 1.0) / 2,
        )
