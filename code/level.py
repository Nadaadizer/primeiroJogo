import random
import time
import pygame
from pygame import font
from code.const import EVENT_ENEMY, SPAWN_TIME, COLOR_WHITE, WIN_W, WIN_H
from code.entityFactory import EntityFactory

class Level:
    def __init__(self, window, name, game_mode):
        self.enemy_scaling_count = 0
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.player = EntityFactory.get_entity('player')
        self.entity_list = EntityFactory.get_entity('level1bg')
        self.entity_enemy_list = []
        self.arrow_list = []

        self.start_time = time.time()
        self.last_scaling_time = self.start_time
        self.last_scale_message_time = 0
        self.scale_message_duration = 3

        self.current_run_time = 0
        self.best_time = 0
        self.partidas_jogadas = 0
        self.last_heal_time = -30

        self.enemy_base_hp_multiplier = 1.0
        self.enemy_base_damage_multiplier = 1.0

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def save_progress(self):
        with open("save.txt", "w") as file:
            file.write(f"{self.player.level},{self.player.xp},{self.player.next_xp},{self.partidas_jogadas},{int(self.best_time)},{self.player.direction}\n")

    def load_progress(self):
        try:
            with open("save.txt", "r") as file:
                data = file.readline().strip().split(",")
                self.player.level = int(data[0])
                self.player.xp = int(data[1])
                self.player.next_xp = int(data[2])
                self.partidas_jogadas = int(data[3])
                self.best_time = int(data[4])
                if len(data) > 5:
                    self.player.direction = data[5]
                print(f"Save carregado: LVL {self.player.level}, XP {self.player.xp}/{self.player.next_xp}, Partidas: {self.partidas_jogadas}, Melhor tempo: {self.best_time}s")
        except:
            pass

    def run(self):
        global camera_x

        self.enemy_base_hp_multiplier = 1.0
        self.enemy_base_damage_multiplier = 1.0
        self.start_time = time.time()
        self.last_scaling_time = self.start_time
        self.enemy_scaling_count = 0

        self.load_progress()
        self.partidas_jogadas += 1

        pygame.mixer_music.load('./asset/Level.mp3')
        pygame.mixer_music.set_volume(0.03)
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()
        running = True
        paused = False

        while running:
            dt = clock.tick(60) / 1000.0
            now = time.time()
            self.current_run_time = now - self.start_time

            if now - self.last_scaling_time >= 20:
                self.enemy_scaling_count += 1
                self.last_scaling_time = now
                self.last_scale_message_time = now
                print(f"[ESCALAMENTO] Escalamento #{self.enemy_scaling_count} (x{1 + 0.75 * self.enemy_scaling_count})")

            self.player.stamina = min(self.player.stamina + (4 * dt), 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_progress()
                    pygame.quit()
                    quit()

                if event.type == EVENT_ENEMY and not paused:
                    if len(self.entity_enemy_list) < 10:
                        offset = random.randint(300, 500)
                        x_spawn = self.player.float_x + random.choice([offset, -offset])
                        y_spawn = WIN_H - 75
                        enemy_type = random.choice(['skeleton', 'werewolf'])
                        enemy = EntityFactory.get_entity_enemy(enemy_type, (x_spawn, y_spawn))

                        scale = 1 + (0.75 * self.enemy_scaling_count)
                        enemy.hp = int(enemy.base_hp * scale)
                        enemy.attack_damage = int(enemy.base_damage * scale)
                        enemy.arrow_damage = int(2 * scale)

                        self.entity_enemy_list.append(enemy)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    if event.key == pygame.K_SPACE and self.player.stamina >= 5:
                        self.player.play_attack_animation()
                        for enemy in self.entity_enemy_list[:]:
                            if abs(enemy.float_x - self.player.float_x) < 40:
                                enemy.hp -= self.player.attack_damage
                                if enemy.hp <= 0:
                                    self.player.add_xp(enemy.xp_reward)
                                    self.entity_enemy_list.remove(enemy)
                        self.player.stamina -= 5
                    if event.key == pygame.K_r:
                        if now - self.last_heal_time >= 30 and self.player.stamina >= 1:
                            self.player.hp = min(self.player.hp + 25, 100)
                            self.last_heal_time = now
                            self.player.stamina -= 3
                            print("Poção usada!")

            if paused:
                self.window.blit(pygame.image.load('./asset/pause_bg.png').convert_alpha(), (0, 0))
                pygame.display.flip()
                continue

            pressed = pygame.key.get_pressed()
            self.player.handle_input(pressed)
            self.player.update_attack_animation()
            camera_x = self.player.float_x

            self.window.fill((0, 0, 0))
            for i in range(-7, 8):
                for bg in self.entity_list:
                    bg.rect.x = int((i * WIN_W) - (camera_x % WIN_W))
                    self.window.blit(bg.surf, bg.rect)

            for arrow in self.arrow_list[:]:
                arrow.move()
                arrow.rect.centerx = int(arrow.float_x - camera_x + WIN_W // 2)
                self.window.blit(arrow.image, arrow.rect)
                if arrow.rect.colliderect(self.player.rect):
                    self.player.hp -= getattr(arrow, 'damage', 2)
                    self.arrow_list.remove(arrow)
                elif arrow.rect.right < 0 or arrow.rect.left > WIN_W:
                    self.arrow_list.remove(arrow)

            for enemy in self.entity_enemy_list[:]:
                enemy.update_behavior(self.player)
                enemy.move_enemy(self.player, self.arrow_list)
                enemy.rect.centerx = int(enemy.float_x - camera_x + WIN_W // 2)
                self.window.blit(enemy.surf, enemy.rect)

            self.player.update_rect()
            self.player.rect.centerx = WIN_W // 2
            self.window.blit(self.player.surf, self.player.rect)

            cooldown_restante = max(0, 30 - (now - self.last_heal_time))
            heal_status = f"Pronto" if cooldown_restante == 0 else f"{int(cooldown_restante)}s"
            self.level_text(
                23,
                f'HP:{self.player.hp} XP:{self.player.xp}/{self.player.next_xp} LVL:{self.player.level} Time:{int(self.current_run_time)}s '
                f'STA:{int(self.player.stamina)}/20 Poção:{heal_status} Escalamentos:{self.enemy_scaling_count}',
                COLOR_WHITE,
                (10, WIN_H - 20)
            )

            if now - self.last_scale_message_time <= self.scale_message_duration:
                escala = f"x1.75 * {self.enemy_scaling_count}"
                self.level_text(40, f'INIMIGOS FORTALECIDOS {escala}', (255, 50, 50), (WIN_W // 2 - 180, 60))

            pygame.display.flip()

            if self.player.hp <= 0:
                xp_bonus = 100 * self.enemy_scaling_count
                if xp_bonus > 0:
                    print(f"XP extra ganho por escalamentos: {xp_bonus}")
                    self.player.add_xp(xp_bonus)
                self.save_progress()
                self.window.blit(pygame.image.load('./asset/game_over.png').convert_alpha(), (0, 0))

                survived_text = f"Tempo sobrevivido: {int(self.current_run_time)}s"
                best_text = f"Melhor tempo: {int(self.best_time)}s"
                self.level_text(36, survived_text, COLOR_WHITE, (WIN_W // 2 - 150, WIN_H - 125))
                self.level_text(30, best_text, (255, 215, 0), (WIN_W // 2 - 130, WIN_H - 150))

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
