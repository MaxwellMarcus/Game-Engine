from game_object import GameObject
from game import Game
from box import Box, Rect
from modifiers import PhysicsBody, Collider
from vector import Vector2
from line import LineSegment, Ray, Line

class Player(GameObject):
    def __init__(self, x: int, y: int) -> None:
        self.pos = Vector2(x, y)
        super().__init__(self.pos, Rect(x, y, 50, 50))

    def update(self, game: Game) -> None:
        if 97 in game.keys:
            self.velocity.x += -1
        if 100 in game.keys:
            self.velocity.x += 1

        if self.pos.y > 490:
            quit()

        super().update(game)


game = Game(500, 500, 'GAME!!!', (0, 0, 0))

player = Player(250, 250)
player.collider = Collider(player.box)
player.physics_body = PhysicsBody(Vector2(0, 1))

floor = GameObject(Vector2(250, 500), Box(250, 500, [
    Vector2(0, 500),
    Vector2(100, 400),
    Vector2(250, 450),
    Vector2(400, 400),
    Vector2(500, 500),
]))
floor.collider = Collider(floor.box)

game.add_gameobject(player)
game.add_gameobject(floor)

box = Rect(250, 500, 500, 50)
p = Rect(250, 475, 50, 50)
print(box.intersects_box(p))

while True: game.update()
