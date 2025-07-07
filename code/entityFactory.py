from code.const import WIN_W, WIN_H
from code.enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'level1bg':
                from code.background import Background
                list_bg = []
                for i in range(5):
                    list_bg.append(Background(f'level1bg{i}', (0, 0)))
                return list_bg
            case 'player':
                from code.player import Player
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
