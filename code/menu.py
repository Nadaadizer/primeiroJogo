#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.const import MENU_OPTION, WIN_W, COLOR_WHITE, COLOR_ORANGE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/BgMenu.png').convert_alpha()
        self.rect = self.surf.get_rect()

        self.surf_tittle = pygame.image.load('./asset/Tittle_Game.png').convert_alpha()
        self.rect_tittle = self.surf_tittle.get_rect()
        self.rect_tittle.centerx = self.window.get_rect().centerx
        self.rect_tittle.top = 50

        self.surf_menu_op1 = pygame.image.load('./asset/Icon_Option.png').convert_alpha()
        self.rect_menu_op1 = self.surf_tittle.get_rect()
        self.rect_menu_op1.centerx = self.window.get_rect().centerx
        self.rect_menu_op1.top = 125

        self.surf_menu_op2 = pygame.image.load('./asset/Icon_Option.png').convert_alpha()
        self.rect_menu_op2 = self.surf_tittle.get_rect()
        self.rect_menu_op2.centerx = self.window.get_rect().centerx
        self.rect_menu_op2.top = 185

        self.surf_menu_op3 = pygame.image.load('./asset/Icon_Option.png').convert_alpha()
        self.rect_menu_op3 = self.surf_tittle.get_rect()
        self.rect_menu_op3.centerx = self.window.get_rect().centerx
        self.rect_menu_op3.top = 245

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.window.blit(source=self.surf_tittle, dest=self.rect_tittle)
            self.window.blit(source=self.surf_menu_op1, dest=self.rect_menu_op1)
            self.window.blit(source=self.surf_menu_op2, dest=self.rect_menu_op2)
            self.window.blit(source=self.surf_menu_op3, dest=self.rect_menu_op3)

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(40, MENU_OPTION[i], COLOR_ORANGE, ((WIN_W / 2), 153 + 60 * i))
                else:
                    self.menu_text(40, MENU_OPTION[i], COLOR_WHITE, ((WIN_W / 2), 153 + 60 * i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_SPACE:  # SPACE KEY
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
