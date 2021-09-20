from vector import Vector2
import pygame
from box import Box, Renderable
from modifiers import Collider

class GameObject:
    pos: Vector2
    velocity: Vector2
    modifiers: list
    box: Box
    renderable: Renderable

    def __init__(self, box: Box, collider: bool = True):
        self.pos = box.pos
        self.velocity = Vector2(0, 0)
        self.box = box
        self.renderable = Renderable(box)
        self.collider = Collider(self, self.box, dynamic=False) if collider else None
        self.physics_body = None

    def _update(self, game) -> None:

        self.update(game)

        if self.physics_body: self.physics_body.update(game)
        if self.collider: self.collider.update(game)

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

    def update(self, game: 'Game'):
        '''Additionally update the GameObject'''
