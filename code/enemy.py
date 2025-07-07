# code/enemy.py
import pygame
import random
import time
from code.entity import Entity
from code.arrow import Arrow
from code.const import ENTITY_SPEED, ENEMY_VISION_RANGE

class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.name = name
        self.speed = ENTITY_SPEED.get(name, 1)
        self.vision_range = ENEMY_VISION_RANGE.get(name, 150)
        self.attack_cooldown = 1.0
        self.last_attack_time = 0
        self.direction = 'right'
        self.state = 'patrol'

        self.walk_images = []
        self.attack_images = []

        if name == 'skeleton':
            self.base_hp = 24
            self.base_damage = 3
            self.xp_reward = 15
            self.walk_images = [pygame.image.load(f'./asset/skeleton_walk{i}.png').convert_alpha() for i in range(1, 9)]
            self.attack_images = [pygame.image.load(f'./asset/skeleton_attack{i}.png').convert_alpha() for i in range(1, 13)]
        elif name == 'werewolf':
            self.base_hp = 41
            self.base_damage = 7
            self.xp_reward = 30
            self.walk_images = [pygame.image.load(f'./asset/werewolf_walk{i}.png').convert_alpha() for i in range(1, 12)]
            self.attack_images = [pygame.image.load(f'./asset/werewolf_attack{i}.png').convert_alpha() for i in range(1, 5)]

        self.hp = self.base_hp
        self.attack_damage = self.base_damage
        self.arrow_damage = 2

        self.current_frame = 0
        self.last_frame_update = time.time()
        self.frame_rate = 0.15
        self.attacking = False

    def apply_scaling(self, scaling_count):
        factor = 1 + 0.75 * scaling_count
        self.hp = int(self.base_hp * factor)
        self.attack_damage = int(self.base_damage * factor)
        self.arrow_damage = int(2 * factor)

    def update_behavior(self, player):
        distance = abs(self.float_x - player.float_x)
        if distance < self.vision_range:
            self.state = 'chase'
        else:
            self.state = 'patrol'

    def move_enemy(self, player, arrow_list):
        now = pygame.time.get_ticks() / 1000.0
        if self.state == 'chase':
            if self.name == 'skeleton':
                if abs(self.float_x - player.float_x) < 100:
                    if self.float_x < player.float_x:
                        self.float_x -= self.speed
                        self.direction = 'left'
                    else:
                        self.float_x += self.speed
                        self.direction = 'right'

                if now - self.last_attack_time >= self.attack_cooldown:
                    arrow = Arrow(self.float_x, self.rect.centery, player.float_x, damage=self.arrow_damage)
                    arrow_list.append(arrow)
                    self.last_attack_time = now
                    self.play_attack_animation()
            else:
                if self.float_x < player.float_x:
                    self.float_x += self.speed
                    self.direction = 'right'
                else:
                    self.float_x -= self.speed
                    self.direction = 'left'

                if abs(self.float_x - player.float_x) < 20:
                    if now - self.last_attack_time >= self.attack_cooldown:
                        player.hp -= self.attack_damage
                        self.last_attack_time = now
                        self.play_attack_animation()
        elif self.state == 'patrol':
            self.float_x += random.choice([-1, 1]) * self.speed * 0.5

        if self.attacking:
            self.update_animation(self.attack_images)
        else:
            self.update_animation(self.walk_images)

        self.update_rect()

    def play_attack_animation(self):
        self.attacking = True
        self.current_frame = 0
        self.last_frame_update = time.time()

    def update_animation(self, images):
        now = time.time()
        if now - self.last_frame_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(images)
            self.last_frame_update = now
        img = images[self.current_frame]
        if self.direction == 'left':
            img = pygame.transform.flip(img, True, False)
        self.surf = img

    def move(self):
        pass
