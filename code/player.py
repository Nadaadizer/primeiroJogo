import pygame
import time
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
        self.direction = 'right'

        self.walk_images = [pygame.image.load(f'./asset/player_walk{i}.png').convert_alpha() for i in range(1, 9)]
        self.attack_images = [pygame.image.load(f'./asset/player_attack{i}.png').convert_alpha() for i in range(1, 5)]
        self.current_frame = 0
        self.last_frame_update = time.time()
        self.frame_rate = 0.1
        self.attacking = False
        self.attack_start_time = 0

    def handle_input(self, pressed_key):
        moved = False
        if pressed_key[pygame.K_d]:
            self.float_x += self.speed
            self.direction = 'right'
            moved = True
        if pressed_key[pygame.K_a]:
            self.float_x -= self.speed
            self.direction = 'left'
            moved = True

        if moved:
            self.update_animation(self.walk_images)
        elif not self.attacking:
            self.surf = self.walk_images[0]

    def update_animation(self, images):
        now = time.time()
        if now - self.last_frame_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(images)
            self.last_frame_update = now
        img = images[self.current_frame]
        if self.direction == 'left':
            img = pygame.transform.flip(img, True, False)
        self.surf = img

    def play_attack_animation(self):
        self.attacking = True
        self.attack_start_time = time.time()
        self.current_frame = 0  # Reinicia animação

    def update_attack_animation(self):
        if self.attacking:
            self.update_animation(self.attack_images)
            if self.current_frame == len(self.attack_images) - 1:
                self.attacking = False

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.next_xp:
            self.xp -= self.next_xp
            self.level += 1
            self.next_xp = int(self.next_xp * 1.5)
            print(f"Nível UP! Agora você está no nível {self.level}.")

    def move(self):
        pass