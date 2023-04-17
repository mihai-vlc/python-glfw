from typing import Any
import glfw
import moderngl
import numpy as np
import math
from python_glfw.logger import logger

def vertices():
    x = np.linspace(-1.0, 1.0, 50)
    y = np.random.rand(50) - 0.5
    r = np.ones(50)
    g = np.arange(0, 1, 0.02)
    b = np.zeros(50)
    a = np.zeros(50)
    return np.dstack([x, y, r, g, b, a])

class HelloWorld2D:
    def __init__(self, ctx: moderngl.Context, reserve: str='4MB'):
        self.ctx = ctx
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

        self.vbo = ctx.buffer(reserve=reserve, dynamic=True)
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert', 'in_color')

    def pan(self, pos):
        self.prog['Pan'].value = pos

    def relative_pan(self, relative_pos):
        pos = self.prog['Pan'].value
        self.prog['Pan'].value = (pos[0] + relative_pos[0], pos[1] + relative_pos[1])

    def clear(self, color=(0, 0, 0, 0)):
        self.ctx.clear(*color)

    def plot(self, points, type='line'):
        data = points.astype('f4').tobytes()
        self.vbo.orphan()
        self.vbo.write(data)
        if type == 'line':
            self.ctx.line_width = 5.0
            self.vao.render(moderngl.LINE_STRIP, vertices=len(data) // 24)
        if type == 'points':
            self.ctx.point_size = 3.0
            self.vao.render(moderngl.POINTS, vertices=len(data) // 24)



def run():

    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1000, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    logger.error(glfw.get_version_string())

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    ctx = moderngl.create_context()
    canvas = HelloWorld2D(ctx)
    verts = vertices()


    def key_callback(window: Any, key: int, scancode: int, action: int, mods: int):
        nonlocal verts
        if action == glfw.RELEASE:
            return

        if key == glfw.KEY_LEFT:
            canvas.relative_pan((-0.1, 0))
        
        if key == glfw.KEY_RIGHT:
            canvas.relative_pan((0.1, 0))

        if key == glfw.KEY_ENTER:
            verts = vertices()
        

    glfw.set_key_callback(window, key_callback)


    def window_size_callback(window: Any, w: int, h: int):
        ctx.fbo.viewport = (0, 0, w, h)

    glfw.set_window_size_callback(window, window_size_callback)

    last_update = 0

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Input
        time = glfw.get_time()

        # Update
        if (time - last_update) > 2:
            last_update = time
            verts = vertices()

        # Render here, e.g. using moderngl
        # canvas.clear(background_color)
        ctx.clear(
            0,
            0,
            (math.sin(time) + 1.0) / 2,
            # (math.sin(time + 10) + 1.0) / 2,
            # (math.sin(time + 30) + 1.0) / 2,
        )
        canvas.plot(verts, type="line")

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    run()
