from abc import ABC, abstractmethod
import pygame
from code.const import ENTITY_SPEED


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = ENTITY_SPEED.get(name, 1)
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

    @abstractmethod
    def move(self):
        pass

    def update_behavior(self, rect):
        pass

    def move_enemy(self, player_rect):
        pass

    def update_rect(self):
        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)
