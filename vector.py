import math

class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def set_length(self, length: float) -> None:
        '''Set the length of the vector to a given value'''
        m = length / self.get_length()
        self.x, self.y = self.x * m, self.y * m
        return self

    def get_length(self) -> float:
        '''Get the length of the vector'''
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(other.x - self.x, other.y - self.y)

    def __iadd__(self, other: 'Vector2') -> 'Vector2':
        return self.__add__(other)

    def __isub__(self, other: 'Vector2') -> 'Vector2':
        return self.__sub__(other)

    def __str__(self) -> str:
        return str((self.x, self.y))

    def __mul__(self, other: float) -> 'Vector2':
        if type(other) in (int, float):
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError(f'Can not multiply {type(self)} by a non scalar of type {type(other)}')
