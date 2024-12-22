from settings import *


class MovementHandler:

    def __init__(self, tool):
        self.movements = []
        self.tool = tool

    def move_linear_relative(self, end_pos: np.ndarray((3), dtype="int16")):

        # we're using bresenhams algorithm for finding the movements in 3d space

        x1, y1, z1 = self.tool.position[0], self.tool.position[1], self.tool.position[2]
        x2, y2, z2 = x1 + end_pos[0], y1 + end_pos[1], z1 + end_pos[2]

        last_x, last_y, last_z = x1, y1, z1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dz = abs(z2 - z1)

        if x2 > x1:
            xs = 1
        else:
            xs = -1

        if y2 > y1:
            ys = 1
        else:
            ys = -1

        if z2 > z1:
            zs = 1
        else:
            zs = -1

        if dx >= dy and dx >= dz:
            p1 = 2 * dy - dx
            p2 = 2 * dz - dx

            while x1 != x2:
                x1 += xs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dx

                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dx

                p1 += 2 * dy
                p2 += 2 * dz

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1

        elif dy >= dx and dy >= dz:
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy

            while y1 != y2:
                y1 += ys
                if p1 >= 0:
                    x1 += xs
                    p1 -= 2 * dy

                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dy

                p1 += 2 * dx
                p2 += 2 * dz

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1

        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz

            while z1 != z2:
                z1 += zs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dz

                if p2 >= 0:
                    x1 += xs
                    p2 -= 2 * dz

                p1 += 2 * dy
                p2 += 2 * dx

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1

    def move_linear_absolute(self, end_pos: np.ndarray((3), dtype="int16")):

        # we're using bresenhams algorithm for finding the movements in 3d space

        x1, y1, z1 = self.tool.position[0], self.tool.position[1], self.tool.position[2]
        x2, y2, z2 = end_pos[0], end_pos[1], end_pos[2]

        last_x, last_y, last_z = x1, y1, z1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dz = abs(z2 - z1)

        if x2 > x1:
            xs = 1
        else:
            xs = -1

        if y2 > y1:
            ys = 1
        else:
            ys = -1

        if z2 > z1:
            zs = 1
        else:
            zs = -1

        if dx >= dy and dx >= dz:
            p1 = 2 * dy - dx
            p2 = 2 * dz - dx

            while x1 != x2:
                x1 += xs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dx

                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dx

                p1 += 2 * dy
                p2 += 2 * dz

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1

        elif dy >= dx and dy >= dz:
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy

            while y1 != y2:
                y1 += ys
                if p1 >= 0:
                    x1 += xs
                    p1 -= 2 * dy

                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dy

                p1 += 2 * dx
                p2 += 2 * dz

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1

        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz

            while z1 != z2:
                z1 += zs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dz

                if p2 >= 0:
                    x1 += xs
                    p2 -= 2 * dz

                p1 += 2 * dy
                p2 += 2 * dx

                # x1,y1,z1 are our last point
                self.movements.append(
                    np.array([x1 - last_x, y1 - last_y, z1 - last_z], dtype="int16")
                )
                last_x, last_y, last_z = x1, y1, z1
