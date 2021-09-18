import pygame
from game_object import GameObject
from typing import Callable
import time

class Game:
    def __init__(self, width:int, height:int, name: str, background: str) -> None:
        '''Initialize Game Class'''
        self.name = name
        self.width, self.height = width, height
        self.background = background

        self.time = time.time()

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))

        self.keys = []

        self.key_events = {}

        self.objects = []

    def add_gameobject(self, object: GameObject) -> None:
        '''Adds a game object to the list of registered game objects'''
        self.objects.append(object)

    def remove_gameobject(self, object: GameObject) -> None:
        '''Removes a game object from the list of registered game objects'''
        self.objects.remove(object)

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
            object.update(self)

        #Render Game Objects
        self.render()

    def render(self) -> None:
        '''Clear the screen and render the Game'''

        self.surface.fill(self.background)

        for object in self.objects:
            object.render().render(self.surface)

        pygame.display.update()
