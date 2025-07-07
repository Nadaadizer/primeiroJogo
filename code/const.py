import pygame

WIN_W = 576
WIN_H = 324

MENU_OPTION = ('Play', 'Upgrade', 'Exit')

COLOR_WHITE = (255, 255, 255)
COLOR_ORANGE = (232, 112, 32)

ENTITY_SPEED = {
    'level1bg0': 0,
    'level1bg1': 1,
    'level1bg2': 0,
    'level1bg3': 0,
    'level1bg4': 2,
    'player': 1.2,
    'skeleton': 0.7,
    'werewolf': 1.3,
}

EVENT_ENEMY = pygame.USEREVENT + 1
SPAWN_TIME = 2000

ENEMY_VISION_RANGE = {
    'skeleton': 200,
    'werewolf': 250,
}

ENEMY_STATS = {
    'skeleton': {
        'hp': 30,
        'damage': 3,
        'xp': 15
    },
    'werewolf': {
        'hp': 55,
        'damage': 7,
        'xp': 30
    }
}
