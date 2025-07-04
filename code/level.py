#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.display

from code.entity import Entity
from code.entityFactory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('level1bg'))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)
                ent.move()

            pygame.display.flip()
            clock.tick(66)  # Limita a 60 quadros por segundo

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
