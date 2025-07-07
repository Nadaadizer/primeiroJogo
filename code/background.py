#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.const import WIN_W, ENTITY_SPEED
from code.entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        pass  # movimento agora é feito pela câmera
