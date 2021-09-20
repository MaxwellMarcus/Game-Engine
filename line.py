from vector import Vector2
from abc import ABC, abstractmethod


class LineType(ABC):
    vertical: bool = False
    m: float 
    b: float 

    def intersects(self, line: 'LineType') -> Vector2:
        '''Returns the point where another line intersects'''
        if self.vertical and line.vertical:
            return self.p1.x == line.p1.x

        elif self.vertical:
            p = Vector2(self.p1.x, line.m * self.p1.x + line.b)

        elif line.vertical:
            p = Vector2(line.p1.x, self.m * line.p1.x + self.b)

        elif not line.m - self.m :
            return self.b == line.b

        elif not line.m:
            p = Vector2((line.b - self.b) / self.m, line.b)

        elif not self.m:
            p = Vector2((self.b - line.b) / line.m, self.b)

        else:
            y = ((line.m * self.b) - (self.m * line.b)) / (line.m - self.m)
            x = (y - line.b) / line.m
            p = Vector2(x, y)
            
        return p if self.in_domain(p) and line.in_domain(p) else None

    def __call__(self, x: float) -> float:
        return self.m * x + self.b if self.in_domain(x) else None

    def __str__(self) -> str:
        return (f'y = ({self.m})x + {self.b}' if not self.vertical else f'x = {self.p1.x}') + f' if x is in {self.domain()}'

    def __eq__(self, other: 'LineType'):
        return other and self.m == other.m and self.b == other.b and self.domain() == other.domain()

    @abstractmethod
    def domain(self) -> list:
        '''Returns the domain of the function as a list'''

    @abstractmethod
    def in_domain(self, p:Vector2) -> bool:
        '''Returns true if a point is in a line types domain'''

class LineSegment(LineType):
    def __init__(self, p1: Vector2, p2: Vector2) -> None:
        self.p1, self.p2 = min([p1, p2], key=lambda i: i.x), max([p1, p2], key=lambda i: i.x)

        self.m, self.b = None, None

        if self.p2.x - self.p1.x == 0:
            self.vertical = True
            self.p1, self.p2 = p1, p2
        else:
            self.m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            self.b = -self.p1.x * self.m + self.p1.y

    def domain(self) -> list:
        return [self.p1.x, self.p2.x, self.p1.y, self.p2.y]

    def in_domain(self, p: Vector2) -> bool:
        return self.p1.x <= p.x <= self.p2.x and (not self.vertical or self.p1.y <= p.y <= self.p2.y or self.p2.y <= p.y <= self.p1.y)


class Line(LineType):
    def __init__(self, m: float, b: float) -> None:
        self.m, self.b = m, b
        self.p1 = Vector2(0, self.b)
        self.p2 = Vector2(1, self.b + self.m)

    def domain(self) -> list:
        return ['-Infinity', 'Infinity']

    def in_domain(self, p: Vector2) -> bool:
        return True

class Ray(LineType):
    def __init__(self, p1: Vector2, m: float) -> None:
        self.p1 = p1

        self.m = m
        self.b = -self.p1.x * self.m + self.p1.y

        self.p2 = Vector2(self.p1.x + 1, self.p1.y + self.m)

    def domain(self) -> list:
        return [self.p1.x, 'Infinity']

    def in_domain(self, p: Vector2) -> bool:
        return self.p1.x <= p.x
