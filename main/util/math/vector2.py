class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        else:
            raise TypeError(f"Unsupported operand type for +: Vector2 and {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        else:
            raise TypeError(f"Unsupported operand type for -: Vector2 and {type(other)}")

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / scalar, self.y / scalar)
        else:
            raise ValueError("Division by zero")

    def __pow__(self, exponent):
        return Vector2(pow(self.x, exponent), pow(self.y, exponent))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def lerp(self, target, interpolation_rate: float):
        self.x = (1 - interpolation_rate) * self.x + interpolation_rate * target.x
        self.y = (1 - interpolation_rate) * self.y + interpolation_rate * target.y
        return self

    def copy(self):
        return Vector2(self.x, self.y)

    @classmethod
    def up(cls):
        return Vector2(0, 1)

    @classmethod
    def down(cls):
        return Vector2(0, -1)

    @classmethod
    def left(cls):
        return Vector2(-1, 0)

    @classmethod
    def right(cls):
        return Vector2(1, 0)

    @classmethod
    def zero(cls):
        return Vector2(0, 0)