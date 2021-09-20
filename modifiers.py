from abc import ABC, abstractmethod
from box import Box
from vector import Vector2

class Modifier(ABC):

    @abstractmethod
    def update(self, game: 'Game') -> None:
        '''Updates and modifies gameobject'''

class PhysicsBody(Modifier):
    def __init__(self, obj: 'GameObject', g: Vector2, f: float=0.8) -> None:
        self.obj = obj

        self.gravity = g
        self.friction = f

    def update(self, game: 'Game') -> None:
        '''Apply physics to Game Object'''

        if not self.obj.collider:
            raise ColliderError('Game Object must have a Collider to have a Physics Body')

        #Gravity
        # if not obj.collider.collided:
        self.obj.velocity += self.gravity * game.delta_time

class Collider(Modifier):
    '''
    Collider for GameObject
    :param box: The Object containing the verticies and lines that make up the collider
    :param dynamic: Specifies if the collider needs to be updated (If the GameObject it is attatched to is static then it doesn't need to change the velocity of the GameObject)
    '''
    def __init__(self, obj: 'GameObject', box:Box, dynamic:bool = True, collidable:bool = True) -> None:
        
        self.obj = obj

        self.box = box
        self.dynamic = dynamic
        self.collidable = collidable

        self.collisions = []

    def set_pos(self, v: Vector2) -> None:
        self.box.set_pos(v)

    def update(self, game: 'Game') -> None:
        '''Check and apply collisions'''
        if not self.dynamic: return 

        self.box.set_pos(self.obj.pos)

        self.collisions = []


        if self.collidable:
            c = self.get_velocity(game)
            self.obj.velocity = c
        else:
            self.collisions = self._is_collided(game.get_collidable())[1]


    def get_velocity(self, game: 'Game'):
        '''Gets the new velocity that accounts for collisions'''
        
        #Check if the position in the next frame will be colliding with another Game Object
        self.box.set_pos(self.obj.pos + self.obj.velocity * game.delta_time)

        others = game.get_collidable()
        lines, self.collisions = self._is_collided(others)

        if not lines: return self.obj.velocity

        self.box.set_pos(Vector2(self.obj.pos.x + self.obj.velocity.x * game.delta_time, self.obj.pos.y))
        collide_x = self._is_collided(self.collisions)[0]

        self.box.set_pos(Vector2(self.obj.pos.x, self.obj.pos.y + self.obj.velocity.y * game.delta_time))
        collide_y = self._is_collided(self.collisions)[0]

        if not (collide_x and collide_y):
            print('X: ', collide_x)
            print('Y: ', collide_y)
            if collide_x:
                return Vector2(0, self.obj.velocity.y)
            
            return Vector2(self.obj.velocity.x, 0)
        
        for l in lines:
            v = self.check_velocity(game, l, lines)
            if v: 
                break
            v = Vector2(0, 0)

        return v

    def check_velocity(self, game: 'Game', line: 'LineType', lines: list) -> Vector2:
        '''Returns Velocity that doesn't allow collider to intersect with another collider'''
        v = Vector2(1, line.m).set_length(self.obj.velocity.x) if not line.vertical else Vector2(0, self.obj.velocity.y)
        self.box.set_pos(self.obj.pos + v * game.delta_time)
        for i in lines:
            if not i is line and self.box.intersects_line(i):
                return None

        return v

    def _is_collided(self, others: list) -> list:
        '''Returns the lines that are intersecting between self and another object if they are at the boxes current position'''
        collisions = []
        chosen = []
        for o in others:
            if o.collider and not o is self.obj:
                b = o.collider
                lines = self.box.intersects_box(b.box)
                if lines:
                    collisions.append(o)
                    if not chosen: chosen = lines
        return chosen, collisions

class ColliderError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
