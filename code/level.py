import random
import time
import pygame
from pygame import Surface, Rect, font
from code.const import EVENT_ENEMY, SPAWN_TIME, COLOR_WHITE, WIN_W, WIN_H
from code.entityFactory import EntityFactory

class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.player = EntityFactory.get_entity('player')
        self.entity_list = EntityFactory.get_entity('level1bg')
        self.entity_enemy_list = []
        self.start_time = time.time()
        self.current_run_time = 0
        self.best_time = 0
        self.partidas_jogadas = 0
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def save_progress(self):
        with open("save.txt", "w") as file:
            file.write(f"{self.player.level},{self.player.xp},{self.player.next_xp},{self.partidas_jogadas},{int(self.best_time)}\n")

    def load_progress(self):
        try:
            with open("save.txt", "r") as file:
                data = file.readline().strip().split(",")
                self.player.level = int(data[0])
                self.player.xp = int(data[1])
                self.player.next_xp = int(data[2])
                self.partidas_jogadas = int(data[3])
                self.best_time = int(data[4])
                print(f"Save carregado: LVL {self.player.level}, XP {self.player.xp}/{self.player.next_xp}, Partidas: {self.partidas_jogadas}, Melhor tempo: {self.best_time}s")
        except:
            pass

    def run(self):
        self.load_progress()
        self.partidas_jogadas += 1
        self.start_time = time.time()

        pygame.mixer_music.load('./asset/Level.mp3')
        pygame.mixer_music.set_volume(0.03)
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()
        running = True
        paused = False

        while running:
            dt = clock.tick(60) / 1000.0
            self.current_run_time = time.time() - self.start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == EVENT_ENEMY and not paused:
                    if len(self.entity_enemy_list) < 10:
                        offset = random.randint(300, 500)
                        x_spawn = self.player.float_x + random.choice([offset, -offset])
                        y_spawn = WIN_H - 75
                        enemy_type = random.choice(['skeleton', 'werewolf'])
                        enemy = EntityFactory.get_entity_enemy(enemy_type, (x_spawn, y_spawn))

                        # Escala inimigo com o tempo
                        escala = 1 + (self.current_run_time // 10) * 0.1
                        enemy.hp = int(enemy.base_hp * escala)
                        enemy.attack_damage = int(enemy.base_damage * escala)

                        self.entity_enemy_list.append(enemy)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    if not running and event.key == pygame.K_SPACE:
                        return

            if paused:
                self.window.blit(pygame.image.load('./asset/pause_bg.png').convert_alpha(), (0,0))
                self.level_text(40, "PAUSADO", COLOR_WHITE, (WIN_W//2 - 60, WIN_H//2))
                pygame.display.flip()
                continue

            pressed = pygame.key.get_pressed()
            self.player.handle_input(pressed)

            camera_x = self.player.float_x
            self.window.fill((0,0,0))

            for i in range(-7, 8):
                for bg in self.entity_list:
                    bg.rect.x = int((i * WIN_W) - (camera_x % WIN_W))
                    self.window.blit(bg.surf, bg.rect)

            for enemy in self.entity_enemy_list[:]:
                enemy.update_behavior(self.player)
                enemy.move_enemy(self.player)
                enemy.rect.centerx = int(enemy.float_x - camera_x + WIN_W //2)
                self.window.blit(enemy.surf, enemy.rect)

                # Player ataca
                if pressed[pygame.K_SPACE]:
                    if abs(enemy.float_x - self.player.float_x) < 40:
                        enemy.hp -= self.player.attack_damage
                        if enemy.hp <= 0:
                            self.player.add_xp(enemy.xp_reward)
                            self.entity_enemy_list.remove(enemy)

            self.player.update_rect()
            self.player.rect.centerx = WIN_W //2
            self.window.blit(self.player.surf, self.player.rect)

            self.level_text(25, f'HP: {self.player.hp} XP: {self.player.xp}/{self.player.next_xp} LVL: {self.player.level} Time: {int(self.current_run_time)}s', COLOR_WHITE, (10, WIN_H-20))
            pygame.display.flip()

            if self.player.hp <= 0:
                if self.current_run_time > self.best_time:
                    self.best_time = self.current_run_time
                self.save_progress()
                self.window.blit(pygame.image.load('./asset/game_over.png').convert_alpha(), (0,0))
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            return

    def level_text(self, text_size, text, color, pos):
        f = font.SysFont("Lucida Sans Typewriter", text_size)
        surf = f.render(text, True, color).convert_alpha()
        rect = surf.get_rect(left=pos[0], top=pos[1])
        self.window.blit(surf, rect)
