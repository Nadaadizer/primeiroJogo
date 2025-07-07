from code.const import WIN_W, WIN_H
from code.enemy import Enemy
from code.player import Player
from code.background import Background

class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'level1bg':
                return [Background(f'level1bg{i}', (i * WIN_W, 0)) for i in range(5)]
            case 'player':
                return Player('player', (WIN_W / 2 - 50, WIN_H - 75))
        return None

    @staticmethod
    def get_entity_enemy(entity_name_enemy: str, position=(0, 0)):
        match entity_name_enemy:
            case 'skeleton':
                return Enemy('skeleton', position)
            case 'werewolf':
                return Enemy('werewolf', position)
        return None
