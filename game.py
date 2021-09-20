import pygame
from game_object import GameObject
from typing import Callable, List
import time

class Game:
    def __init__(self, width:int, height:int, name: str, background: str) -> None:
        '''Initialize Game Class'''
        self.name = name
        self.width, self.height = width, height
        self.background = background

        self.time = time.time()

        pygame.init()

        if not self.width or not self.height:
            display_info = pygame.display.Info()
            self.width, self.height = display_info.current_w, display_info.current_h

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.keys = []

        self.key_events = {}

        self.objects = []

    def add_gameobject(self, *args: List[GameObject]) -> None:
        '''Adds a game object(s) to the list of registered game objects'''
        for obj in args:
            self.objects.append(obj)

    def remove_gameobject(self, obj: GameObject) -> None:
        '''Removes a game object from the list of registered game objects'''
        self.objects.remove(obj)

    def get_collidable(self):
        '''Gets the Game Objects that can be collided with'''
        return filter(lambda o: o.collider and o.collider.collidable, self.objects)

    def add_key_event(self, f: Callable, key: str):
        '''Registers a function to a key event'''
        if key in self.key_events:
            self.key_events[key].append(f)

        else:
            self.key_events[key] = [f]

    def update(self) -> None:
        '''Update the Game'''

        self.delta_time = time.time() - self.time
        self.time = time.time()

        #Record Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                self.keys.append(event.key)

            elif event.type == pygame.KEYUP:
                while event.key in self.keys:
                    self.keys.remove(event.key)

            elif event.type == pygame.QUIT: quit()

        #Call key events
        for key in self.keys:
            if not key in self.key_events: continue
            for event in self.key_events[key]:
                event()

        #Update game objects
        for object in self.objects:
            object._update(self)

        #Render Game Objects
        self.render()

    def render(self) -> None:
        '''Clear the screen and render the Game'''

        self.surface.fill(self.background)

        for object in self.objects:
            object.render().render(self.surface)

        pygame.display.update()
