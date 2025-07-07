import pygame
from pygame import font
from code.const import WIN_W, WIN_H, COLOR_WHITE

class Upgrade:
    def __init__(self, window, player):
        self.window = window
        self.player = player
        self.options = [
            {"label": "Aumentar Dano (+1)", "action": self.up_strength},
            {"label": "Aumentar Vida Max (+10)", "action": self.up_life},
            {"label": "Aumentar Stamina Max (+2)", "action": self.up_stamina},
            {"label": "Aumentar Cura da Poção (+5)", "action": self.up_heal_amount}
        ]
        self.selected = 0
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.window.fill((30, 30, 30))

            self.draw_text(30, "TELA DE UPGRADES", COLOR_WHITE, (WIN_W // 2 - 150, 50))
            self.draw_text(20, f"XP Disponível: {self.player.xp}", COLOR_WHITE, (WIN_W // 2 - 100, 100))

            for i, option in enumerate(self.options):
                color = (255, 215, 0) if i == self.selected else COLOR_WHITE
                self.draw_text(26, option["label"], color, (WIN_W // 2 - 150, 160 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.options[self.selected]["action"]()

    def draw_text(self, size, text, color, pos):
        f = font.SysFont("Lucida Sans Typewriter", size)
        surf = f.render(text, True, color)
        rect = surf.get_rect(topleft=pos)
        self.window.blit(surf, rect)

    def up_strength(self):
        if self.player.xp >= 100:
            self.player.attack_damage += 1
            self.player.xp -= 100
            print("[UPGRADE] Dano aumentado para:", self.player.attack_damage)

    def up_life(self):
        if self.player.xp >= 100:
            self.player.max_hp += 10
            self.player.hp = self.player.max_hp
            self.player.xp -= 100
            print("[UPGRADE] Vida máxima aumentada para:", self.player.max_hp)

    def up_stamina(self):
        if self.player.xp >= 100:
            self.player.max_stamina += 2
            self.player.xp -= 100
            print("[UPGRADE] Stamina máxima aumentada para:", self.player.max_stamina)

    def up_heal_amount(self):
        if self.player.xp >= 100:
            self.player.heal_amount += 5
            self.player.xp -= 100
            print("[UPGRADE] Quantidade de cura aumentada para:", self.player.heal_amount)
