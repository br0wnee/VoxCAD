from settings import *
from meshes.chunk_mesh_builder import get_chunk_index
from world_objects.tool import Tool
from movement_handler import MovementHandler
from numba import njit


defined_movements = [
    [0, -CHUNK_SIZE - CHUNK_SIZE // 2, 0],
    [CHUNK_SIZE * 4, 0, 0],
    [0, 0, CHUNK_SIZE * 4],
    [CHUNK_SIZE * 4, 0, 0],
]


class ToolHandler:

    def __init__(self, world):

        self.world = world
        self.app = world.app
        self.tool = Tool()
        self.mv_handler = MovementHandler(self.tool)

        self.init_tool()

        for movement in defined_movements:
            self.mv_handler.move_linear_relative(np.array(movement, dtype="int16"))

        self.d_time = 0

        self.mvID = 0
        self.movements = self.mv_handler.movements

        self.simulation_done = False

    def init_tool(self):
        self.tool_action(Operation.REMOVE)
        self.tool_action(Operation.ADD)

    def move_tool(self):
        self.tool_action(Operation.REMOVE)
        self.tool.position += self.movements[self.mvID]
        self.tool_action(Operation.ADD)
        self.mvID += 1

    def update(self):

        if not self.simulation_done:
            self.tool_action(Operation.REMOVE)
            self.tool.position += self.movements[self.mvID]
            self.tool_action(Operation.ADD)
            self.mvID += 1
            if self.mvID == len(self.movements):
                self.simulation_done = True

    def affected_chunks(self) -> np.ndarray:

        arr = []

        x0, y0, z0 = (
            self.tool.position[0] - self.tool.dimensions[0] // 2,
            self.tool.position[1],
            self.tool.position[2] - self.tool.dimensions[2] // 2,
        )

        for x in range(MOST_AFFECTED_CHUNKS_W):
            for y in range(MOST_AFFECTED_CHUNKS_H):
                for z in range(MOST_AFFECTED_CHUNKS_D):

                    chunk_index = get_chunk_index(
                        (
                            x0 + x * CHUNK_SIZE,
                            y0 + y * CHUNK_SIZE,
                            z0 + z * CHUNK_SIZE,
                        )
                    )

                    if 0 <= chunk_index < WORLD_VOL:
                        arr.append(chunk_index)

        return np.array(arr)

    def tool_action(self, operation: Operation):

        a_chunks = self.affected_chunks()
        tool_to_chunks(
            affected_chunks=np.array(a_chunks, dtype="int32"),
            voxels=self.world.voxels,
            tool_position=self.tool.position,
            tool_dimensions=self.tool.dimensions,
            operation=int(operation),
        )

        for chunk in a_chunks:
            self.world.chunks[chunk].build_mesh()


@njit
def tool_to_chunks(
    affected_chunks,
    voxels,
    tool_position,
    tool_dimensions,
    operation,
    CHUNK_SIZE=CHUNK_SIZE,
):

    start_x = tool_position[0] - tool_dimensions[0] // 2
    start_y = tool_position[1]
    start_z = tool_position[2] - tool_dimensions[2] // 2
    end_x = start_x + tool_dimensions[0]
    end_y = start_y + tool_dimensions[1]
    end_z = start_z + tool_dimensions[2]

    # Calculate the radius of the cylinder (radius = tool_dimensions[0] / 2)
    cylinder_radius = tool_dimensions[0] / 2

    for chunkID in affected_chunks:
        chunk = voxels[chunkID]

        chunk_start_x = (chunkID % WORLD_W) * CHUNK_SIZE
        chunk_start_y = (chunkID // (WORLD_AREA)) * CHUNK_SIZE
        chunk_start_z = ((chunkID // WORLD_W) % WORLD_D) * CHUNK_SIZE

        chunk_end_x = chunk_start_x + CHUNK_SIZE
        chunk_end_y = chunk_start_y + CHUNK_SIZE
        chunk_end_z = chunk_start_z + CHUNK_SIZE

        # Calculate overlapping region
        overlap_start_x = max(start_x, chunk_start_x)
        overlap_end_x = min(end_x, chunk_end_x)
        overlap_start_y = max(start_y, chunk_start_y)
        overlap_end_y = min(end_y, chunk_end_y)
        overlap_start_z = max(start_z, chunk_start_z)
        overlap_end_z = min(end_z, chunk_end_z)

        if (
            overlap_start_x < overlap_end_x
            and overlap_start_y < overlap_end_y
            and overlap_start_z < overlap_end_z
        ):
            # Modify voxels inside the cylindrical shape
            for x in range(overlap_start_x, overlap_end_x):
                for y in range(overlap_start_y, overlap_end_y):
                    for z in range(overlap_start_z, overlap_end_z):
                        # Check if (x, z) are inside the cylindrical radius
                        dx = x - tool_position[0]
                        dz = z - tool_position[2]
                        distance = math.sqrt(dx**2 + dz**2)

                        # If the point is inside the cylindrical radius and within the height
                        if distance <= cylinder_radius:
                            # Local chunk coordinates
                            chunk_local_x = x - chunk_start_x
                            chunk_local_y = y - chunk_start_y
                            chunk_local_z = z - chunk_start_z

                            # Modify voxel data
                            chunk_index = (
                                chunk_local_x
                                + CHUNK_SIZE * chunk_local_z
                                + CHUNK_AREA * chunk_local_y
                            )
                            if operation == 1:
                                chunk[chunk_index] = 3
                            elif operation == 0:
                                chunk[chunk_index] = 0
