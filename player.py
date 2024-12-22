from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app

        super().__init__(position, yaw, pitch)

    def update(self):
        super().update()

    def handle_tool_control(self, key, action, modifiers):

        keys = self.app.wnd.keys
        tool = self.app.scene.world.tool_handler.tool

        keys_pressed = self.app.keys_pressed

        if keys_pressed.get(keys.LEFT):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([-1, 0, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.RIGHT):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([1, 0, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.UP):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 0, -1], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.DOWN):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 0, 1], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.TAB):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, -1, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.SPACE):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 1, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)

        if keys_pressed.get(keys.M):
            self.app.scene.world.tool_handler.move_tool()

    def mouse_control(self, dx, dy):
        if dx:
            self.rotate_yaw(delta_x=dx * MOUSE_SENSITIVITY)
        if dy:
            self.rotate_pitch(delta_y=dy * MOUSE_SENSITIVITY)

    def keyboard_control(self, key, action, modifiers):
        keys = self.app.wnd.keys

        vel = PLAYER_SPEED * self.app.delta_time

        if action == keys.ACTION_PRESS:
            if key == keys.W:
                self.move_forward(vel)
            if key == keys.S:
                self.move_back(vel)
            if key == keys.D:
                self.move_right(vel)
            if key == keys.A:
                self.move_left(vel)
            if key == keys.E:
                self.move_up(vel)
            if key == keys.Q:
                self.move_down(vel)
