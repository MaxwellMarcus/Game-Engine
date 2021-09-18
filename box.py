from line import Line, LineSegment, Ray
from vector import Vector2
import pygame

class Box:
    def __init__(self, x: float, y: float, verticies: list) -> None:
        self.pos = Vector2(x, y)
        self.verticies = verticies
        self.lines = self._get_lines()

    def _get_lines(self) -> list:
        lines = []
        for i in range(len(self.verticies)):
            lines.append(LineSegment(self.verticies[i], self.verticies[(i + 1) % len(self.verticies)]))

        return lines

    def intersects_point(self, p: Vector2) -> bool:
        '''Check if Box contains a point'''
        intersections = 0
        horizontal = Ray(p, 1)
        for line in self.lines:
            if line.intersects(horizontal): intersections += 1
        return bool(intersections % 2)

    def intersects_box(self, b: 'Box') -> bool:
        '''Check if Box intersects with another'''
        for line1 in self.lines:
            for line2 in b.lines:
                if line1.intersects(line2): return (line1, line2)
        return None

    def set_pos(self, v: Vector2):
        '''Move box by a given amount'''
        change = v - self.pos
        self.pos = v
        for i in self.verticies:
            i += change

        self.lines = self._get_lines()

    def vector_to_list(self) -> list:
        self.lines = self._get_lines()
        l = []
        for i in self.verticies:
            l.append([i.x, i.y])
        return l

    def __str__(self) -> str:
        return str([str(v) for v in self.verticies])

class Rect(Box):
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.pos, self.size = Vector2(x, y), Vector2(width, height)
        super().__init__(x, y, self.get_verticies())

    def get_verticies(self) -> list:
        '''Gets the verticies of the rectangle from position width and height'''
        return [
            Vector2(self.pos.x - self.size.x / 2, self.pos.y - self.size.y / 2),
            Vector2(self.pos.x - self.size.x / 2, self.pos.y + self.size.y / 2),
            Vector2(self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2),
            Vector2(self.pos.x + self.size.x / 2, self.pos.y - self.size.y / 2),
        ]

    def set_pos(self, v: Vector2) -> None:
        '''Set position of the Rectangle'''
        self.pos = v
        self.verticies = self.get_verticies()

class Renderable:
    def __init__(self, box: Box, color: str = 'white') -> None:
        self.color = color
        self.box = box

    def set_pos(self, v: Vector2) -> None:
        self.box.set_pos(v)

    def __list__(self) -> list:
        return self.box.vector_to_list()

    def render(self, surface: pygame.Surface) -> None:
        '''Render Verticies'''
        pygame.draw.polygon(surface, self.color, self.box.vector_to_list())
