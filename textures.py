import moderngl as mgl
from settings import *
from PIL import Image


class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # load texture
        self.texture_0 = self.load("frame.png")

        # assign texture unit
        self.texture_0.use(location=0)

    def load(self, file_name):

        try:
            image = Image.open(f"assets/{file_name}")
        except FileNotFoundError:
            print(f"Image file not found: {file_name}")
            return None

        image = image.convert("RGBA")

        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        texture = self.ctx.texture(
            size=image.size,
            components=4,
            data=image.tobytes(),
        )

        texture.anisotropy = 8.0
        texture.build_mipmaps()
        texture.filter = (mgl.LINEAR, mgl.LINEAR)
        return texture
