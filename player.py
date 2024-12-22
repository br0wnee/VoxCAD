import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app

        self.controller_connected = False

        if pg.joystick.get_count() >= 1:
            self.init_controller()
        super().__init__(position, yaw, pitch)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        if self.controller_connected:
            self.gamepad_movement_xz()
        super().update()

    def handle_tool_control(self, event):

        tool = self.app.scene.world.tool_handler.tool

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_LEFT:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([-1, 0, 0], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_RIGHT:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([1, 0, 0], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_UP:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([0, 0, -1], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_DOWN:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([0, 0, 1], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_TAB:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([0, -1, 0], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_SPACE:
                self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
                tool.position += np.array([0, 1, 0], dtype="int16")
                self.app.scene.world.tool_handler.tool_action(Operation.ADD)

            if event.key == pg.K_m:
                self.app.scene.world.tool_handler.move_tool()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)
        if key_state[pg.K_q]:
            self.move_up(vel)
        if key_state[pg.K_e]:
            self.move_down(vel)

    def init_controller(self):

        self.controller = pg.joystick.Joystick(0)
        self.local_x_delta = 0
        self.local_z_delta = 0
        self.controller_connected = True

    def gamepad_movement_xz(self):

        tool = self.app.scene.world.tool_handler.tool

        horiz_move = self.controller.get_axis(0)
        vert_move = self.controller.get_axis(1)

        if abs(horiz_move) > 0.05:
            self.local_z_delta += horiz_move / 10.0

        if abs(vert_move) > 0.05:
            self.local_x_delta += vert_move / 10.0

        if self.local_x_delta > 1.0:

            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 0, 1], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
            self.local_x_delta = 0

        elif self.local_x_delta < -1.0:

            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 0, -1], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
            self.local_x_delta = 0

        elif self.local_z_delta > 1.0:

            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([1, 0, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
            self.local_z_delta = 0

        elif self.local_z_delta < -1.0:

            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([-1, 0, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
            self.local_z_delta = 0

    def gamepad_movement_y(self, event):

        tool = self.app.scene.world.tool_handler.tool

        if event.type == pg.JOYBUTTONDOWN and self.controller.get_button(4):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, 1, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
        if event.type == pg.JOYBUTTONDOWN and self.controller.get_button(5):
            self.app.scene.world.tool_handler.tool_action(Operation.REMOVE)
            tool.position += np.array([0, -1, 0], dtype="int16")
            self.app.scene.world.tool_handler.tool_action(Operation.ADD)
