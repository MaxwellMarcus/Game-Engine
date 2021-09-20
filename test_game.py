from game import Game
from box import Box, Rect
from modifiers import PhysicsBody, Collider
from vector import Vector2
from line import LineSegment, Ray, Line
import pygame
from game_object import GameObject

class Player(GameObject):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(Rect(x, y, 50, 50))

        self.direction = 1

        self.physics_body = PhysicsBody(self, Vector2(0, 1000))
        self.collider.dynamic = True

        self.renderable.color = 'blue'

        self.bullet_time = 0
        self.bullet_delay = 0.5

    def update(self, game: Game) -> None:
        
        self.velocity.x = 0
        if pygame.K_a in game.keys:
            self.velocity.x = -200
            self.direction = -1
        elif pygame.K_d in game.keys:
            self.velocity.x = 200
            self.direction = 1

        if pygame.K_w in game.keys and self.collider.collisions:
            self.velocity.y = -500

        if pygame.K_SPACE in game.keys and game.time - self.bullet_time > self.bullet_delay:
            self.bullet_time = game.time
            game.add_gameobject(Projectile(self.pos, Vector2(self.direction * 500, 0)))

        super().update(game)

class Projectile(GameObject):
    def __init__(self, pos: Vector2, velocity: Vector2):
        super().__init__(Rect(pos.x, pos.y, 10, 5))
        self.velocity = velocity

        self.renderable.color = 'red'

        self.collider.dynamic = True
        self.collider.collidable = False

    def update(self, game: Game):
        if 0 > self.pos.x < game.width:
            game.remove_gameobject(self)

        for obj in self.collider.collisions:
            if not type(obj) == Player:
                game.remove_gameobject(self) 

game = Game(0, 0, 'GAME!!!', (0, 0, 0)) 

player = Player(250, 250)

floor = GameObject(Box(game.width / 2, game.height, [
    Vector2(0, game.height),
    Vector2(game.width / 3 - 150, game.height - 200),
    Vector2(game.width / 3 + 100, game.height - 50),
    Vector2(game.width / 2 - 50, game.height - 400),
    Vector2(game.width / 2 + 50, game.height - 400),
    Vector2(2 * game.width / 3 - 150, game.height - 50),
    Vector2(2 * game.width / 3 + 100, game.height - 200),
    Vector2(game.width, game.height)
]))

platforms = [
    GameObject(Rect(game.width / 3, game.height - 250, 50, 5)),
    GameObject(Rect(game.width / 3 + 200, game.height - 350, 50, 5)),
    GameObject(Rect(2 * game.width / 3, game.height - 250, 50, 5)),
    GameObject(Rect(2 * game.width / 3 - 200, game.height - 350, 50, 5)),
]

game.add_gameobject(player)
game.add_gameobject(floor)
game.add_gameobject(*platforms)

while True: game.update()
