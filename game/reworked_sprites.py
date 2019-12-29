"""
Created on 2019-12-29

Project: shooter
@author: ollejernstrom
"""
import pygame

vec = pygame.math.Vector2


class Use:
    pass


# Sets all keybindings
class KeyHandler:
    def __init__(self, key_list):
        # KEY ORDER: LEFT, RIGHT, UP, DOWN, PICKUP, DROP, THROW, SHOOT
        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_jump = key_list[2]
        self.key_down = key_list[3]
        self.key_pickup = key_list[4]
        self.key_drop = key_list[5]
        self.key_throw = key_list[6]
        self.key_shoot = key_list[7]


class Physics:
    def __init__(self):
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        pass


class Jump:
    pass

class Drop:
    pass

class Throw:
    pass

class Move:
    def __init__(self, thing_to_move):
        self.moveable = thing_to_move

    def move_left(self):
        self.acc.x = -self.

    def move_right(self):


class Player:
    def __init__(self, keylist):
        self.use = Use()
        self.keys = KeyHandler(keylist)
        self.physics = Physics()
        self.jumpaction = Jump
        self.movement = Move


    def update(self):
        # Should physics update return pos or operate directly on pos
        self.physics.update()

        keys = pygame.keys.get_pressed()
        if keys[self.keys.key_jump]:
            self.jumpaction()

        if keys[self.keys.key_left]:
