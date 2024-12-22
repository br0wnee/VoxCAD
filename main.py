from settings import *
import moderngl as mgl
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures
from ui import UI
import moderngl_window as mglw
from moderngl_window import WindowConfig


from imgui_bundle import imgui
from moderngl_window.integrations.imgui_bundle import ModernglWindowRenderer


class VoxCAD(WindowConfig):
    title = "VoxCAD"
    window_size = (WIN_WIDTH, WIN_HEIGHT)
    resizable = False
    cursor = False

    vsync = False
    gl_version = (4, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.wnd.ctx.error
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.ui = UI(self)

        self.delta_time = 0
        self.time = 0

        self.keys_pressed = {}
        self.wnd.mouse_exclusivity = True

        self.is_running = True

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.timer._frames

    def on_render(self, time: float, frametime: float):
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = "auto"

        self.ctx.clear(color=BG_COLOR)
        self.update()
        self.scene.render()
        self.ui.render()
        self.wnd.swap_buffers()

    def on_key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            self.keys_pressed[key] = True
        elif action == keys.ACTION_RELEASE:
            self.keys_pressed[key] = False

        self.player.keyboard_control(key, action, modifiers)
        self.player.handle_tool_control(key, action, modifiers)

    def on_mouse_position_event(self, x, y, dx, dy):
        self.player.mouse_control(dx, dy)


if __name__ == "__main__":
    mglw.run_window_config(VoxCAD)
