#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import pygame as pg

from code.const import WIN_H, WIN_W
from code.menu import Menu


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_W, WIN_H))

    def run(self, ):

        while True:
            menu = Menu(self.window)
            menu.run()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
