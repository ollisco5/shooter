import math
import operator
import pygame.math

class VectorError(Exception):
    pass

class Vector2(object):
    def __init__(self, x: object, y: object) -> object:
        self.x = x
        self.y = y


    def add(self, vector2):
        try:
            if type(vector2) != type(Vector2):
                raise VectorError()
            return Vector2(self.x + vector2.x, self.y + vector2.y)

        except VectorError as e:
            print(e)






class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

