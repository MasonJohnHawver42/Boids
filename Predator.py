from Xlib import display
from Vehicle import *


class Predator(Vehicle):
    def __init__(self, x, y, world):
        Vehicle.__init__(self, x, y, world)
        self.threat_dis = 100
        self.hunt_dis = 140
        self.sep_dis = self.size + 20
        self.maxSpeed = 25
        self.maxForce = 3

    def run(self):
        self.behaviours()
        Vehicle.run(self)

    def behaviours(self):
        atk = self.attack(self.world.boids)
        ret = self.rebound()
        sep = self.separate(self.world.predators)

        atk.mult(Vector(50, 50))
        ret.mult(Vector(5, 5))
        sep.mult(Vector(10, 10))

        self.applyForce(atk)
        self.applyForce(ret)
        self.applyForce(sep)

        self.acc.limitMag(self.maxForce)

    def attack(self, boids):
        sum = Vector(0, 0)
        count = 0
        for boid in boids:
            distance = Vector.getDis(self.pos, boid.pos)
            if distance < self.hunt_dis:
                sum.add(boid.pos)
                count += 1

        if count > 0:
            sum.div(Vector(count, count))
            return self.seek(sum)

        else:
            return Vector(0, 0)

    def separate(self, preds):
        count = 0
        steer = Vector(0, 0)
        for boid in preds:
            dis = Vector.getDis(self.pos, boid.pos)
            if boid != self and (dis < self.sep_dis):
                diff = Vector.subTwo(self.pos, boid.pos)
                steer.add(diff)

        if count > 0:
            steer.div(Vector(count, count))

        if steer.getMag() > 0:
            steer.setMag(self.maxSpeed)
            steer.sub(self.vel)
            steer.limitMag(self.maxForce)
            steer.mult(Vector(-1, -1))

        return steer

    def draw(self, arr):
        x, y = (int(self.pos.x), int(self.pos.y))
        verts = self.getVerts()

        cv2.fillConvexPoly(arr, verts.reshape((-1, 1, 2)),
                           [100, 100] + [mapNum(self.vel.getMag(), 0, self.maxSpeed, 51, 255)])

        for i in range(verts.shape[0]):
            vert1 = verts[i]
            vert2 = verts[(i + 1) % verts.shape[0]]

            cv2.line(arr, (vert1[0], vert1[1]), (vert2[0], vert2[1]), (0, 0, 255), 2)

        if self == self.world.predators[0]:
            cv2.circle(arr, (x, y), self.hunt_dis, (255, 0, 0))
            cv2.circle(arr, (x, y), self.threat_dis, (0, 0, 255))


# mouse stuff
def getMousePos():
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]


def getWindowMousePos(window):
    win_x, win_y, w, h = cv2.getWindowImageRect(window)
    m_x, m_y = getMousePos()

    return Vector(m_x - win_x, m_y - win_y)


class MousePredator(Predator):
    def __init__(self, world):
        Predator.__init__(self, world.center.x, world.center.y, world)
        self.maxSpeed = 100
        self.maxForce = 30

    def run(self):
        self.behaviours()
        self.update()

    def behaviours(self):
        arv = self.arrive(getWindowMousePos(self.world.name))

        arv.mult(Vector(1, 1))

        self.applyForce(arv)

        self.acc.limitMag(self.maxForce)

    def draw(self, arr):
        x, y = (int(self.pos.x), int(self.pos.y))
        cv2.circle(arr, (x, y), self.size, [mapNum(self.vel.getMag(), 0, self.maxSpeed, 51, 255)] * 3, -1)
        cv2.circle(arr, (x, y), self.threat_dis, (0, 0, 255), 1)