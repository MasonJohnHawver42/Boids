from Vector import *


class Vehicle:
    def __init__(self, x, y, world):
        self.pos = Vector(x, y)
        self.vel = Vector(1, 0)
        self.acc = Vector(0, 0)

        self.maxSpeed = 6
        self.maxForce = .5

        self.size = 10  # radius

        self.world = world

    def borders(self):
        if self.pos.x < -self.size:
            self.pos.x = self.world.width + self.size

        elif self.pos.x > self.world.width + self.size:
            self.pos.x = -self.size

        if self.pos.y < -self.size:
            self.pos.y = self.world.height + self.size

        elif self.pos.y > self.world.height + self.size:
            self.pos.y = -self.size

    def run(self):
        self.borders()
        self.update()

    def update(self):
        self.vel.add(self.acc)
        self.vel.limitMag(self.maxSpeed)
        self.pos.sub(self.vel)
        self.acc.set(0, 0)

    def applyForce(self, force):
        # can add mass a = f / m
        self.acc.add(force)

    def seek(self, target):
        desired = Vector.subTwo(self.pos, target)
        desired.setMag(self.maxSpeed)
        steer = Vector.subTwo(desired, self.vel)
        steer.limitMag(self.maxForce)

        return steer

    def arrive(self, target):
        desired = Vector.subTwo(self.pos, target)

        speed = self.maxSpeed
        if desired.getMag() < 100:
            speed = mapNum(desired.getMag(), 0, 100, 0, self.maxSpeed)

        desired.limitMag(speed)

        steer = Vector.subTwo(desired, self.vel)
        steer.limitMag(self.maxForce)

        return steer

    def avoid(self, target):
        steer = self.seek(target)
        return steer.mult(Vector(-1, -1))

    def randomness(self):
        steer = Vector.getRndVec(-1, 1)
        steer.limitMag(self.maxForce)

        return steer

    def rebound(self):
        distance = Vector.getDis(self.pos, self.world.center)
        if distance > self.world.center_dis != 0:
            return self.seek(self.world.center)
        else:
            return Vector(0, 0)


    def getVerts(self):
        verts = np.zeros((4, 2), dtype=int)

        bot_point = self.vel.copy()
        bot_point.setMag(self.size)
        top_point = bot_point.getFliped()

        bot_point.div(Vector(np.sqrt(2), np.sqrt(2)))  # get sqrt 2 from a constant in math lib

        perp = top_point.getPerp()
        right_point = Vector.addTwo(bot_point, perp)
        left_point = Vector.subTwo(bot_point, perp)

        bot_point.mult(Vector(.6, .6))

        verts[0, :] = Vector.addTwo(top_point, self.pos).toArr()
        verts[1, :] = Vector.addTwo(right_point, self.pos).toArr()
        verts[2, :] = Vector.addTwo(bot_point, self.pos).toArr()
        verts[3, :] = Vector.addTwo(left_point, self.pos).toArr()

        return verts

    def draw(self, arr):
        x, y = (int(self.pos.x), int(self.pos.y))
        cv2.circle(arr, (x, y), self.size, [mapNum(self.vel.getMag(), 0, self.maxSpeed, 51, 255)] * 3, -1)