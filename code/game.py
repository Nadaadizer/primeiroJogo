#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import pygame as pg

from code.const import WIN_H, WIN_W, MENU_OPTION
from code.level import Level
from code.menu import Menu


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_W, WIN_H))

    def run(self, ):

        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                level = Level(self.window, "level1", menu_return)
                leve_return = level.run()

            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass