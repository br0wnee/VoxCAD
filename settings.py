from numba import njit
import numpy as np
import glm
import math
from enum import IntEnum

# resolution
WIN_HEIGHT = 900
WIN_WIDTH = 1600
WIN_RES = glm.vec2(WIN_WIDTH, WIN_HEIGHT)

# chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)
# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# workpiece

WORKPIECE_W, WORKPIECE_H, WORKPIECE_D = 16, 4, 16
WORKPIECE_AREA = WORKPIECE_W * WORKPIECE_D
WORKPIECE_VOL = WORKPIECE_AREA * WORKPIECE_H

# world
WORLD_OFFSET_W = 2
WORLD_OFFSET_H = 2
WORLD_OFFSET_D = 2

WORLD_W = WORKPIECE_W + WORLD_OFFSET_W
WORLD_H = WORKPIECE_H + WORLD_OFFSET_H
WORLD_D = WORKPIECE_D + WORLD_OFFSET_D

WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# player
PLAYER_SPEED = 0.5 * 10000
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# tool

# Tool's width and depth need to be odd
TOOL_W = 65
TOOL_H = 32
TOOL_D = 65

# most affected chunks as the tool move

MOST_AFFECTED_CHUNKS_W = math.ceil(TOOL_W / CHUNK_SIZE) + 1
MOST_AFFECTED_CHUNKS_H = math.ceil(TOOL_H / CHUNK_SIZE) + 1
MOST_AFFECTED_CHUNKS_D = math.ceil(TOOL_D / CHUNK_SIZE) + 1

# physical properties

# voxels per 1mm
RESOLUTION = 8
WORKPIECE_REAL_WIDTH = WORKPIECE_W / RESOLUTION
WORKPIECE_REAL_HEIGHT = WORKPIECE_H / RESOLUTION
WORKPIECE_REAL_DEPTH = WORKPIECE_D / RESOLUTION

# tool operations


class Operation(IntEnum):
    ADD = 1
    REMOVE = 0


# colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)
