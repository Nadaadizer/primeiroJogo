#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image


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

    def run(self, ):

        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.window.blit(source=self.surf_tittle, dest=self.rect_tittle)
            self.window.blit(source=self.surf_menu_op1, dest=self.rect_menu_op1)
            self.window.blit(source=self.surf_menu_op2, dest=self.rect_menu_op2)
            self.window.blit(source=self.surf_menu_op3, dest=self.rect_menu_op3)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
