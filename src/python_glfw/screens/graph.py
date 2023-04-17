from typing import Any, Tuple
import moderngl
import numpy as np
import glfw


def vertices():
    x = np.linspace(-1.0, 1.0, 50)
    y = np.random.rand(50) - 0.5
    r = np.ones(50)
    g = np.arange(0, 1, 0.02)
    b = np.zeros(50)
    a = np.zeros(50)
    return np.dstack([x, y, r, g, b, a])


class Graph2DScreen:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.verts = vertices()
        self.last_update = 0
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform vec2 Pan;

                in vec2 in_vert;
                in vec4 in_color;

                out vec4 v_color;

                void main() {
                    v_color = in_color;
                    gl_Position = vec4(in_vert - Pan, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in vec4 v_color;

                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            ''',
        )

        self.vbo = ctx.buffer(reserve='4MB', dynamic=True)  # type: ignore
        self.vao = ctx.simple_vertex_array(
            self.prog, self.vbo, 'in_vert', 'in_color')

    def pan(self, pos):
        self.prog['Pan'].value = pos

    def relative_pan(self, relative_pos):
        pan = self.prog['Pan']
        pos = pan.value
        pan.value = (pos[0] + relative_pos[0], pos[1] + relative_pos[1])

    def clear(self, color: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.ctx.clear(*color)

    def plot(self, points: Any, type: str = 'line'):
        data = points.astype('f4').tobytes()
        self.vbo.orphan()
        self.vbo.write(data)
        if type == 'line':
            self.ctx.line_width = 5.0
            self.vao.render(moderngl.LINE_STRIP, vertices=len(data) // 24)
        if type == 'points':
            self.ctx.point_size = 3.0
            self.vao.render(moderngl.POINTS, vertices=len(data) // 24)

    def key_callback(self, key: int, action: int):
        if action == glfw.RELEASE:
            return

        if key == glfw.KEY_LEFT:
            self.relative_pan((-0.1, 0))

        if key == glfw.KEY_RIGHT:
            self.relative_pan((0.1, 0))

        if key == glfw.KEY_ENTER:
            self.regenerate()

    def regenerate(self):
        self.verts = vertices()

    def update(self, time: float):
        if (time - self.last_update) > 2:
            self.last_update = time
            self.regenerate()

    def render(self):
        self.plot(self.verts)
