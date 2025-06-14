import tkinter as tk
import math
from mathdevs import Vec3, normal_tri


class GfxEngine:
    """
    Графический движок для проецирования и отрисовки 3D объектов.

    Атрибуты:
        width, height — размеры холста
        scale — масштабирование проекции
        cx, cy — центр экрана
        rot_x, rot_y, rot_z — углы поворота вокруг осей
        light_dir — направление источника света
    """

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.scale = 10
        self.cx = width // 2
        self.cy = height // 2
        self.rot_x = self.rot_y = self.rot_z = 0
        self.light_dir = Vec3(1, 1, 1).norm()  # Направление света

    def project(self, pt):
        """
        Проекция точки из 3D пространства на 2D экран с учётом поворотов.

        Параметры:
            pt (Vec3): исходная точка в 3D
        Возвращает:
            tuple: экранные координаты (x, y)
        """
        x, y, z = pt.x, pt.y, pt.z

        # Поворот вокруг осей
        cx, sx = math.cos(self.rot_x), math.sin(self.rot_x)
        y, z = y * cx - z * sx, y * sx + z * cx

        cy, sy = math.cos(self.rot_y), math.sin(self.rot_y)
        x, z = x * cy + z * sy, -x * sy + z * cy

        cz, sz = math.cos(self.rot_z), math.sin(self.rot_z)
        x, y = x * cz - y * sz, x * sz + y * cz

        # Перспективное проецирование
        fov = 320
        dist = 50
        factor = fov / (dist + z)
        px = int(x * factor * self.scale)
        py = int(y * factor * self.scale)

        return self.cx + px, self.cy + py

    def draw_surf(self, canvas, grid, color="#3498db", wireframe=False):
        """
        Отображает поверхность на холсте.

        Параметры:
            canvas (tk.Canvas): целевой холст
            grid (list[list[Vec3]]): сетка точек поверхности
            color (str): цвет заливки
            wireframe (bool): режим отображения (каркас или залитая)
        """
        for i in range(len(grid) - 1):
            for j in range(len(grid[i]) - 1):
                p1 = grid[i][j]
                p2 = grid[i+1][j]
                p3 = grid[i+1][j+1]
                p4 = grid[i][j+1]

                v1 = self.project(p1)
                v2 = self.project(p2)
                v3 = self.project(p3)
                v4 = self.project(p4)

                if wireframe:
                    canvas.create_line(v1, v2, fill="black")
                    canvas.create_line(v2, v3, fill="black")
                    canvas.create_line(v3, v4, fill="black")
                    canvas.create_line(v4, v1, fill="black")
                else:
                    n1 = normal_tri(p1, p2, p3)
                    i1 = self._light(n1)
                    c1 = self._shade(color, i1)
                    canvas.create_polygon(v1 + v2 + v3, fill=c1, outline="")

                    n2 = normal_tri(p1, p3, p4)
                    i2 = self._light(n2)
                    c2 = self._shade(color, i2)
                    canvas.create_polygon(v1 + v3 + v4, fill=c2, outline="")

    def _light(self, normal):
        """Рассчитывает яркость точки на основе нормали и света."""
        dot = normal.dot(self.light_dir)
        return max(0.2, min(1.0, 0.5 + 0.5 * dot))

    def _shade(self, hex_color, intensity):
        """Изменяет цвет в зависимости от интенсивности освещения."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = max(0, min(255, int(r * intensity)))
        g = max(0, min(255, int(g * intensity)))
        b = max(0, min(255, int(b * intensity)))

        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_axes(self, canvas, length=2):
        """Рисует координатные оси XYZ для ориентации."""
        origin = Vec3(0, 0, 0)
        o = self.project(origin)

        x = self.project(Vec3(length, 0, 0))
        y = self.project(Vec3(0, length, 0))
        z = self.project(Vec3(0, 0, length))

        canvas.create_line(o, x, fill="red", width=2)
        canvas.create_text(x, text="X", fill="red")

        canvas.create_line(o, y, fill="green", width=2)
        canvas.create_text(y, text="Y", fill="green")

        canvas.create_line(o, z, fill="blue", width=2)
        canvas.create_text(z, text="Z", fill="blue")