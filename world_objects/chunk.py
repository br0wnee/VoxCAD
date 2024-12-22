from settings import *
from meshes.chunk_mesh import ChunkMesh


class Chunk:
    def __init__(self, world, position, type):
        self.app = world.app
        self.world = world
        self.position = position

        # type indicates whether the chunk is only for tool or tool+workpiece
        self.type = None

        self.m_model = self.get_model_matrix()

        self.voxels: np.array = None
        self.mesh: ChunkMesh = None

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

        self.is_empty = True

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.program["m_model"].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum:
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        # fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    if y < 10:
                        voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 2
                    else:
                        voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 1

        if np.any(voxels):
            self.is_empty = False

        return voxels

    def build_voxels_solid(self):
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 1

        if np.any(voxels):
            self.is_empty = False

        return voxels

    def build_empty(self):
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        self.is_empty = False

        return voxels
