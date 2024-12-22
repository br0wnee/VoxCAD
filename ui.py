from settings import *
import moderngl as mgl

from imgui_bundle import imgui


class UI:

    def __init__(self, app):
        self.app = app

    def render(self):
        imgui.new_frame()

        imgui.begin("Diagnostic", True)
        imgui.text(f"FPS: {self.app.timer.fps_average}")
        imgui.end()

        imgui.render()

        self.app.imgui.render(imgui.get_draw_data())
