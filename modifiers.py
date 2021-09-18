from abc import ABC, abstractmethod
from game_object import GameObject
from box import Box
from vector import Vector2
from game import Game

class Modifier(ABC):

    @abstractmethod
    def update(self, object: GameObject, game: Game) -> None:
        '''Updates and modifies gameobject'''

class PhysicsBody(Modifier):
    def __init__(self, g: Vector2, f: float=0.8) -> None:
        self.gravity = g
        self.friction = f

    def update(self, object: GameObject, game: Game) -> None:
        '''Apply physics to Game Object'''

        if not object.collider:
            raise ColliderError('Game Object must have a Collider to have a Physics Body')

        #Gravity
        object.velocity += self.gravity

        #Friction

class Collider(Modifier):
    def __init__(self, box:Box) -> None:
        self.box = box

    def set_pos(self, v: Vector2) -> None:
        self.box.set_pos(v)

    def update(self, object: GameObject, game: Game) -> None:
        '''Check and apply collisions'''
        others = game.objects

        self.box.set_pos(object.pos)

        self.collided = False

        #Check if the position in the next frame along the x axis will be colliding with another Game Object
        # self.box.set_pos(Vector2(object.pos.x + object.velocity.x * game.delta_time, object.pos.y))
        self.box.set_pos(Vector2(object.pos.x + object.velocity.x, object.pos.y))
        lines = self.is_collided(object, others)
        if lines:
            line = lines[1]
            object.velocity = Vector2(1, line.m).set_length(object.velocity.x) if not line.vertical else Vector2(0, object.velocity.y)
            self.collided = True

        #Check if the position in the next frame along the y axis will be colliding with another Game Object
        self.box.set_pos(Vector2(object.pos.x, object.pos.y + object.velocity.y))
        lines = self.is_collided(object, others)
        if lines:
            object.velocity.y = 0

    def is_collided(self, object: GameObject, others: list) -> list:
        '''Returns the lines that are intersecting between self and another object if they are'''
        for o in others:
            if o.collider and not o is object:
                b = o.collider
                lines = self.box.intersects_box(b.box)
                if lines:
                    return lines
        return []

class ColliderError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
