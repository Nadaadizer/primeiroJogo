#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.background import Background
from code.const import WIN_W


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'level1bg':
                list_bg = []
                for i in range(5):
                    list_bg.append(Background(f'level1bg{i}', (0,0)))
                    list_bg.append(Background(f'level1bg{i}', (WIN_W,0)))
                return list_bg
        return None
