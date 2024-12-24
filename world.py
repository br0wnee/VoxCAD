from settings import *
from world_objects.chunk import Chunk
from tool_handler import ToolHandler


class World:

    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)

        self.build_workpiece_chunks()

        self.build_chunk_mesh()

        self.tool_handler = ToolHandler(self)

    def build_workpiece_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z), type=None)

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # Chunk is within the wokrpiece volume
                    if (
                        (
                            x >= WORLD_OFFSET_W // 2
                            and x < (WORLD_W - (WORLD_OFFSET_W // 2))
                        )
                        and (y >= 0 and y < (WORLD_H - WORLD_OFFSET_H))
                        and (
                            z >= WORLD_OFFSET_D // 2
                            and z < (WORLD_D - (WORLD_OFFSET_D // 2))
                        )
                    ):

                        if y != 0:
                            self.voxels[chunk_index] = chunk.build_voxels_solid()
                        else:
                            self.voxels[chunk_index] = chunk.build_voxels()
                    else:
                        self.voxels[chunk_index] = chunk.build_empty()

                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.tool_handler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
