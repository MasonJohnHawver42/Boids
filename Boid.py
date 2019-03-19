from Vehicle import *


class Boid(Vehicle):

    def __init__(self, x, y, world):
        Vehicle.__init__(self, x, y, world)

        self.ali_dis = 60
        self.sep_dis = self.size + 25
        self.coh_dis = 120

        self.ali_bias = 9
        self.sep_bias = 30
        self.coh_bias = 4
        self.rnd_bias = 1
        self.ret_bias = 40
        self.avd_bias = 10000

        self.age = 0
        self.health = 1
        self.split_age = np.random.randint(500, 1000)

    def run(self):
        self.borders()
        self.update()
        self.flock()
        self.sliderBarUpdate()
        #self.growUp()

    def flock(self):
        ali = self.align(self.world.boids)
        sep = self.separate(self.world.boids)
        coh = self.cohesion(self.world.boids)
        rnd = self.randomness()
        ret = self.rebound()
        avd = self.avoidPredators(self.world.predators)

        ali.mult(Vector(self.ali_bias, self.ali_bias))
        sep.mult(Vector(self.sep_bias, self.sep_bias))
        coh.mult(Vector(self.coh_bias, self.coh_bias))
        rnd.mult(Vector(self.rnd_bias, self.rnd_bias))
        ret.mult(Vector(self.ret_bias, self.ret_bias))
        avd.mult(Vector(self.avd_bias, self.avd_bias))

        self.applyForce(ali)
        self.applyForce(sep)
        self.applyForce(coh)
        self.applyForce(rnd)
        self.applyForce(ret)
        self.applyForce(avd)

        self.acc.limitMag(self.maxForce)

    def sliderBarUpdate(self):
        if self.world.boidTrackball_name != "":
            self.size = cv2.getTrackbarPos("size", self.world.boidTrackball_name)

            self.ali_dis = cv2.getTrackbarPos("ali_dis", self.world.boidTrackball_name)
            self.ali_bias = cv2.getTrackbarPos("ali_bias", self.world.boidTrackball_name)

            self.sep_dis = cv2.getTrackbarPos("sep_dis", self.world.boidTrackball_name)
            self.sep_bias = cv2.getTrackbarPos("sep_bias", self.world.boidTrackball_name)

            self.coh_dis = cv2.getTrackbarPos("coh_dis", self.world.boidTrackball_name)
            self.coh_bias = cv2.getTrackbarPos("coh_bias", self.world.boidTrackball_name)

            self.maxSpeed = cv2.getTrackbarPos("maxSpeed", self.world.boidTrackball_name)
            self.maxForce = cv2.getTrackbarPos("maxForce", self.world.boidTrackball_name) / 100

            # side effects
            self.sep_dis += self.size

    def growUp(self):
        self.age += 1
        if 0 >= self.health or self.age > 1800:
            self.die()

        if self.age == self.split_age:
            print(self.age)
            self.split()

    def split(self):
        newBoid = Boid(self.pos.x, self.pos.y, self.world)
        newBoid.vel = self.vel.copy().mult(Vector(-1, 1))
        self.world.addBoid(newBoid)

    def die(self):
        self.world.boids.remove(self)

    def align(self, boids):
        sum = Vector(0, 0)
        count = 0
        for boid in boids:
            dis = Vector.getDis(self.pos, boid.pos)
            if boid != self and (dis < self.ali_dis):
                sum.add(boid.vel)
                count += 1

        if count > 0:
            sum.div(Vector(count, count))

            sum.setMag(self.maxSpeed)
            steer = Vector.subTwo(sum, self.vel)
            steer.limitMag(self.maxForce)

            return steer

        else:
            return Vector(0, 0)

    def separate(self, boids):
        count = 0
        steer = Vector(0, 0)
        for boid in boids:
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

    def cohesion(self, boids):
        count = 0
        sum = Vector(0, 0)

        for boid in boids:
            dis = Vector.getDis(self.pos, boid.pos)
            if boid != self and dis < self.coh_dis:
                sum.add(boid.pos)
                count += 1

        if count > 0:
            sum.div(Vector(count, count))
            return self.seek(sum)

        else:
            return Vector(0, 0)

    def avoidPredators(self, preds):
        sum = Vector(0, 0)
        count = 0
        for pred in preds:
            distance = Vector.getDis(self.pos, pred.pos)
            if distance < pred.threat_dis:
                sum.add(pred.pos)
                count += 1

            if distance < self.size:
                self.health -= 1

        if count > 0:
            sum.div(Vector(count, count))
            return self.avoid(sum)
        else:
            return Vector(0, 0)

    def draw(self, arr):
        x, y = (int(self.pos.x), int(self.pos.y))
        verts = self.getVerts()

        cv2.fillConvexPoly(arr, verts.reshape((-1, 1, 2)), [mapNum(self.vel.getMag(), 0, self.maxSpeed, 51, 255)] * 3)

        for i in range(verts.shape[0]):
            vert1 = verts[i]
            vert2 = verts[(i + 1) % verts.shape[0]]

            cv2.line(arr, (vert1[0], vert1[1]), (vert2[0], vert2[1]), (0, 0, 0), 2)

        if self == self.world.boids[0]:
            cv2.circle(arr, (x, y), self.coh_dis, (255, 0, 0))
            cv2.circle(arr, (x, y), self.ali_dis, (0, 255, 0))
            cv2.circle(arr, (x, y), self.sep_dis, (0, 0, 255))
