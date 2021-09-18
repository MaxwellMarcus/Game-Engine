from vector import Vector2
import pygame
from box import Box, Renderable

class GameObject:
    pos: Vector2
    velocity: Vector2
    modifiers: list
    box: Box
    renderable: Renderable

    def __init__(self, pos: Vector2, box: Box):
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.box = box
        self.renderable = Renderable(box)
        self.collider = None
        self.physics_body = None

    def update(self, game) -> None:

        if self.physics_body: self.physics_body.update(self, game)
        if self.collider: self.collider.update(self, game)

        self.pos += self.velocity * game.delta_time

    def set_velocity(self, v):
        self.velocity = v

    def set_pos(self, v):
        self.pos = v

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def render(self) -> Renderable:
        '''Returns a renderable polygon'''
        self.renderable.set_pos(self.pos)
        return self.renderable
