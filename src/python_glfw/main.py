from typing import Any
import glfw
import moderngl
import math
from python_glfw.logger import logger
from python_glfw.screens import Graph2DScreen


def run():

    # Initialize the library
    if not glfw.init():
        logger.error("Failed to initialize glfw")
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        1000, 600, "My Awesome Application", None, None)

    if not window:
        glfw.terminate()
        return

    logger.info(glfw.get_version_string())

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    ctx = moderngl.create_context()
    canvas = Graph2DScreen(ctx)

    def key_callback(window: Any, key: int, scancode: int, action: int, mods: int):
        canvas.key_callback(key, action)

    glfw.set_key_callback(window, key_callback)

    def window_size_callback(window: Any, w: int, h: int):
        ctx.fbo.viewport = (0, 0, w, h)

    glfw.set_window_size_callback(window, window_size_callback)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Input
        time = glfw.get_time()

        # Update
        canvas.update(time)

        # Render here, e.g. using moderngl
        # canvas.clear(background_color)
        ctx.clear(
            0,
            0,
            (math.sin(time) + 1.0) / 2,
            # (math.sin(time + 10) + 1.0) / 2,
            # (math.sin(time + 30) + 1.0) / 2,
        )
        canvas.render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    run()
