import random
import pygame
from code.entity import Entity
from code.const import ENTITY_SPEED, ENEMY_VISION_RANGE

class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.speed = ENTITY_SPEED.get(name, 1)
        self.vision_range = ENEMY_VISION_RANGE.get(name, 150)
        self.attack_cooldown = 1.0
        self.last_attack_time = 0

        if name == 'skeleton':
            self.base_hp = 30
            self.base_damage = 3
            self.xp_reward = 15
        elif name == 'werewolf':
            self.base_hp = 55
            self.base_damage = 7
            self.xp_reward = 30

        self.hp = self.base_hp
        self.attack_damage = self.base_damage
        self.state = 'patrol'

    def move(self):
        pass

    def update_behavior(self, player):
        distance = abs(self.float_x - player.float_x)
        if distance < self.vision_range:
            self.state = 'chase'
        else:
            self.state = 'patrol'

    def move_enemy(self, player):
        if self.state == 'chase':
            if self.name == 'skeleton':
                # Ataca de longe (simulação do tiro)
                now = pygame.time.get_ticks() / 1000.0
                if now - self.last_attack_time >= self.attack_cooldown:
                    if abs(self.float_x - player.float_x) < self.vision_range:
                        player.hp -= self.attack_damage
                        self.last_attack_time = now
                        print(f"{self.name} disparou flecha! HP do player: {player.hp}")
            else:
                if self.float_x < player.float_x:
                    self.float_x += self.speed
                else:
                    self.float_x -= self.speed

                if abs(self.float_x - player.float_x) < 20:
                    now = pygame.time.get_ticks() / 1000.0
                    if now - self.last_attack_time >= self.attack_cooldown:
                        player.hp -= self.attack_damage
                        self.last_attack_time = now
                        print(f"{self.name} atacou! HP do player: {player.hp}")
        elif self.state == 'patrol':
            self.float_x += random.choice([-1, 1]) * self.speed * 0.5

        self.update_rect()
