import numpy as np
import math
import cv2


def clip(n, min_n, max_n):
    return min(max(n, min_n), max_n)

def mapNum(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def invert(num, max):
    return (num - max) * -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def mult(self, other):
        self.x *= other.x
        self.y *= other.y
        return self

    def div(self, other):
        if other.x == 0:
            self.x = 0
        else:
            self.x /= other.x
        if other.y == 0:
            self.y = 0
        else:
            self.y /= other.y
        return self

    def set(self, x, y):
        self.x = x
        self.y = y

    def getMag(self):
        return np.sqrt((self.x ** 2) + (self.y ** 2))

    def normalize(self):
        if self.x == 0:
            if self.y != 0:
                self.y = self.y / abs(self.y)

        else:
            x = np.sqrt(1 / (((self.y ** 2) / (self.x ** 2)) + 1)) * (self.x / abs(self.x))
            y = (x * self.y) / self.x
            self.set(x, y)

    def setMag(self, mag):
        self.normalize()
        self.mult(Vector(mag, mag))

    def limitMag(self, mag):
        if self.getMag() >= mag:
            self.setMag(mag)

    def getPerp(self):
        x = self.y * -1
        y = self.x
        return Vector(x, y)

    def getFliped(self):
        return Vector(self.x * -1, self.y * -1)

    def toArr(self):
        """converts vector into an array: x, y"""
        return np.array([self.x, self.y])

    def toTuple(self):
        """converts vector into a tuple: x, y"""
        return (self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

    @staticmethod
    def addTwo(vec1, vec2):
        return Vector(vec1.x + vec2.x, vec1.y + vec2.y)

    @staticmethod
    def subTwo(vec1, vec2):
        return Vector(vec1.x - vec2.x, vec1.y - vec2.y)

    @staticmethod
    def getDis(vec1, vec2):
        return Vector.subTwo(vec1, vec2).getMag()

    @staticmethod
    def getRndVec(min, max):
        return Vector(np.random.randint(min, max), np.random.randint(min, max))

    def __repr__(self):
        return str(self.x) + " / " + str(self.y)

    def __str__(self):
        return str(self.x) + " / " + str(self.y)

