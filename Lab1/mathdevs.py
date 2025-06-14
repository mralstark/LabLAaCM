import math


class Vec3:
  
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        """Скалярное произведение двух векторов."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Векторное произведение двух векторов (результат перпендикулярен обоим)."""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def mag(self):
        """Длина (модуль) вектора."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def norm(self):
        """Нормализация вектора (приведение к единичной длине)."""
        length = self.mag()
        if length == 0:
            return Vec3()
        return self * (1.0 / length)


def normal_tri(a, b, c):
    
    v1 = b - a
    v2 = c - a
    return v1.cross(v2).norm()


def generate(func, u_range, v_range, u_steps=50, v_steps=30, **kwargs):
    """
    Генерирует двумерную сетку точек поверхности по параметрической функции.

    Параметры:
        func (callable): функция вида f(u, v, ...) -> Vec3
        u_range (tuple): диапазон изменения параметра u (start, end)
        v_range (tuple): диапазон изменения параметра v (start, end)
        u_steps (int): количество шагов по параметру u
        v_steps (int): количество шагов по параметру v
        **kwargs: дополнительные аргументы для func
    Возвращает:
        list[list[Vec3]]: двумерная сетка точек
    """
    umin, umax = u_range
    vmin, vmax = v_range
    du = (umax - umin) / u_steps
    dv = (vmax - vmin) / v_steps

    grid = []
    for i in range(u_steps + 1):
        row = []
        u = umin + i * du
        for j in range(v_steps + 1):
            v = vmin + j * dv
            row.append(func(u, v, **kwargs))
        grid.append(row)
    return grid


def helix(u, v, alpha=0.5, beta=0.5, zlim=0.5):
    """
    Параметрическая функция для винтовой поверхности.

    Параметры:
        u (float): угол/радиус
        v (float): высота
        alpha (float): радиальный масштаб
        beta (float): вертикальный масштаб
        zlim (float): ограничение по высоте
    Возвращает:
        Vec3: точка на поверхности
    """
    r = u
    x = alpha * r * math.cos(u)
    y = beta * r * math.sin(u)
    z = max(-zlim, min(zlim, v))  # Ограничение значения Z
    return Vec3(x, y, z)