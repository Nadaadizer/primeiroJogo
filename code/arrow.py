import pygame

class Arrow:
    def __init__(self, x, y, target_x, damage=2):
        self.image = pygame.image.load('./asset/arrow.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.float_x = x
        self.speed = 5
        self.direction = 1 if target_x > x else -1
        self.damage = damage

    def move(self):
        self.float_x += self.speed * self.direction
        self.rect.centerx = int(self.float_x)

    def draw(self, window, camera_x):
        draw_x = self.rect.centerx - camera_x + (576 // 2)
        window.blit(self.image, (draw_x, self.rect.y))
