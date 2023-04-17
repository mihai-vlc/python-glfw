
import moderngl
import cairo
import math
from array import array

from .component import Component


class Text(Component):
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.texture = self.render_cairo_to_texture(1980, 1080)
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_position;
            in vec2 in_texcoord_0;
            out vec2 uv;
            void main() {
                gl_Position = vec4(in_position, 1.0);
                uv = in_texcoord_0;
            }
            """,
            fragment_shader="""
            #version 330
            uniform sampler2D texture0;
            in vec2 uv;
            out vec4 outColor;
            void main() {
                outColor = texture(texture0, uv);
            }
            """,
        )
        # Create a simple screen rectangle. The texture coordinates
        # are reverted on the y axis here to make the cairo texture appear correctly.
        vertices = [
            # x, y | u, v
            -1,  1,  0, 0,
            -1, -1,  0, 1,
            1,  1,  1, 0,
            1, -1,  1, 1,
        ]
        self.screen_rectangle = self.ctx.vertex_array(
            self.prog,
            [
                (
                    self.ctx.buffer(array('f', vertices)),
                    '2f 2f',
                    'in_position', 'in_texcoord_0',
                )
            ],
        )

    def update(self, delta_time: float):
        pass

    def key_callback(self, key: int, action: int):
        pass

    def render(self):
        self.texture.use(location=0)
        self.ctx.enable(moderngl.BLEND)
        self.screen_rectangle.render(mode=moderngl.TRIANGLE_STRIP)

    def render_cairo_to_texture(self, width: int, height: int):
        # Draw with cairo to surface
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        ctx.select_font_face("monospace",
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(90)
        ctx.set_source_rgba(1, 0, 0, 1)

        title = "My Awesome Application"
        extents = ctx.text_extents(title)
        ctx.move_to(width/2 - extents.width/2, extents.height)
        ctx.show_text(title)

        # Copy surface to texture
        texture = self.ctx.texture((width, height), 4, data=surface.get_data())
        # use Cairo channel order (alternatively, the shader could do the swizzle)
        texture.swizzle = 'BGRA'
        return texture
