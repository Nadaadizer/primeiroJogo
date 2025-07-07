import pygame
from code.entity import Entity

class Player(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.hp = 100
        self.xp = 0
        self.level = 1
        self.next_xp = 100
        self.attack_damage = 9
        self.stamina = 20

    def handle_input(self, pressed_key):
        if pressed_key[pygame.K_d]:
            self.float_x += self.speed
        if pressed_key[pygame.K_a]:
            self.float_x -= self.speed

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.next_xp:
            self.xp -= self.next_xp
            self.level += 1
            self.next_xp = int(self.next_xp * 1.5)
            print(f"Nível UP! Agora você está no nível {self.level}.")


    def move(self):
        pass