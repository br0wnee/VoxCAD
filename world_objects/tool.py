from settings import *


class Tool:

    def __init__(self):

        # for now, let's not exceed the tool dims beyond the chunk limit of 32
        self.dimensions = np.array([TOOL_W, TOOL_H, TOOL_D], dtype="uint8")

        # world position of the center-bottom point of the tool
        self.position = np.array(
            [CENTER_XZ, WORLD_H * CHUNK_SIZE - TOOL_H, CENTER_XZ], dtype="int32"
        )

    def move_tool(self, movement: np.ndarray(3, dtype="int32")):

        self.position += movement
