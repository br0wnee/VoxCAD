from settings import *
import moderngl as mgl

from imgui_bundle import imgui
from imgui import COLOR_TEXT
from imgui import (
    WINDOW_NO_MOVE,
    WINDOW_NO_RESIZE,
    WINDOW_NO_TITLE_BAR,
    WINDOW_NO_BACKGROUND,
)


class UI:

    def __init__(self, app):
        self.app = app

    def render(self):
        imgui.new_frame()

        # self.information_windows()
        self.create_coordinate_system_widget()

        imgui.render()

        self.app.imgui.render(imgui.get_draw_data())

    def information_windows(self):

        imgui.begin("Diagnostic", True)
        imgui.text(f"FPS: {self.app.timer.fps_average}")
        imgui.end()

        imgui.begin("Tool", True)
        imgui.text(f"Position: {self.app.scene.world.tool_handler.tool.position}")
        imgui.end()

    def create_coordinate_system_widget(self):
        # Extract camera vectors
        right = glm.normalize(self.app.player.right)  # X-axis vector
        up = glm.normalize(self.app.player.up)  # Y-axis vector
        forward = glm.normalize(
            self.app.player.forward
        )  # Z-axis vector (forward direction)

        # Widget size and position
        widget_size = 200
        widget_pos = glm.vec2(WIN_WIDTH - widget_size * 0.5 - 10, 100)

        # Begin ImGui window
        imgui.begin(
            "Coordinate System",
            False,
            flags=WINDOW_NO_MOVE
            | WINDOW_NO_RESIZE
            | WINDOW_NO_TITLE_BAR
            | WINDOW_NO_BACKGROUND,
        )

        # Get ImGui drawing list
        draw_list = imgui.get_window_draw_list()

        # Axis length
        axis_length = widget_size * 0.4

        # Calculate end points for axes
        x_end = widget_pos + glm.vec2(right.x, right.y) * axis_length
        y_end = widget_pos - glm.vec2(up.x, up.y) * axis_length
        z_end = (
            widget_pos - glm.vec2(forward.x, forward.y) * axis_length
        )  # Z-axis typically points forward

        # Draw X-axis (Red)
        draw_list.add_line(
            imgui.ImVec2(widget_pos.x, widget_pos.y),
            imgui.ImVec2(x_end.x, x_end.y),
            imgui.IM_COL32(255, 0, 0, 255),
            4.0,
        )
        # Draw Y-axis (Green)
        draw_list.add_line(
            imgui.ImVec2(widget_pos.x, widget_pos.y),
            imgui.ImVec2(y_end.x, y_end.y),
            imgui.IM_COL32(0, 255, 0, 255),
            4.0,
        )

        # Draw Z-axis (Blue)
        draw_list.add_line(
            imgui.ImVec2(widget_pos.x, widget_pos.y),
            imgui.ImVec2(z_end.x, z_end.y),
            imgui.IM_COL32(0, 0, 255, 255),
            4.0,
        )

        # Add text labels near the ends of the axes
        draw_list.add_text(
            imgui.ImVec2(x_end.x + 5, x_end.y - 5),
            col=imgui.IM_COL32(255, 0, 0, 255),
            text_begin="X",
        )
        draw_list.add_text(
            imgui.ImVec2(y_end.x + 5, y_end.y - 5),
            col=imgui.IM_COL32(0, 255, 0, 255),
            text_begin="Y",
        )
        draw_list.add_text(
            imgui.ImVec2(z_end.x + 5, z_end.y - 5),
            col=imgui.IM_COL32(0, 0, 255, 255),
            text_begin="Z",
        )

        # End ImGui window
        imgui.end()
