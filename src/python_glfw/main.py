from typing import Any
import glfw
import moderngl
from python_glfw.components import Background
from python_glfw.logger import logger
from python_glfw.components import Graph2D
from python_glfw.scenes import Scene


def run():

    if not glfw.init():
        logger.error("Failed to initialize glfw")
        return

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
    active_scene = Scene()

    active_scene.add_component(Background(ctx))
    active_scene.add_component(Graph2D(ctx))

    def key_callback(window: Any, key: int, scancode: int, action: int, mods: int):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        active_scene.key_callback(key, action)

    glfw.set_key_callback(window, key_callback)

    def window_size_callback(window: Any, w: int, h: int):
        ctx.fbo.viewport = (0, 0, w, h)

    glfw.set_window_size_callback(window, window_size_callback)

    delta_time = 0
    last_frame = 0

    while not glfw.window_should_close(window):
        # Input
        time = glfw.get_time()
        delta_time = time - last_frame
        last_frame = time

        # Update
        active_scene.update(delta_time)

        # Render
        active_scene.render()

        glfw.swap_buffers(window)

        # Process pending events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    run()
