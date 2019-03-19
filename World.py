from Boid import *
from Predator import *


class World:
    next_id = 0

    def __init__(self, width, height):
        self.boids = []
        self.predators = []
        self.width = width
        self.height = height

        self.center = Vector(self.width / 2, self.height / 2)
        self.center_dis = 0

        self.boidTrackball_name = ""
        self.trackBar_name = ""
        self.name = "World-" + str(World.next_id)
        cv2.namedWindow(self.name)
        World.next_id += 1

    def toImg(self):  # (w, h)
        img = np.zeros((self.height, self.width, 3)) + 51
        cv2.circle(img, (int(self.center.x), int(self.center.y)), int(self.center_dis), (255, 200, 150), -1)

        for vehicle in self.boids + self.predators:
            vehicle.draw(img)

        return img

    def run(self):
        self.trackbarUpdate()
        for vehicle in self.boids + self.predators:
            vehicle.run()

    def simulate(self):
        while True:
            img = self.toImg()

            cv2.imshow(self.name, img.astype(np.uint8))
            cv2.imshow(self.boidTrackball_name, np.zeros((1, 1, 3)))
            cv2.waitKey(1)

            self.run()



    def trackbarUpdate(self):
        if self.trackBar_name != "":
            self.width = max(cv2.getTrackbarPos("width", self.trackBar_name), 1)
            self.height = max(cv2.getTrackbarPos("height", self.trackBar_name), 1)
            self.center_dis = cv2.getTrackbarPos("center_dis", self.trackBar_name)

            self.center = Vector(self.width / 2, self.height / 2)

    def WorldTrackbars(self):
        self.trackBar_name = "World-" + self.name
        cv2.namedWindow(self.trackBar_name)

        cv2.createTrackbar('width', self.trackBar_name, self.width, 2000, lambda x: None)
        cv2.createTrackbar('height', self.trackBar_name, self.height, 2000, lambda x: None)

        cv2.createTrackbar('center_dis', self.trackBar_name, self.center_dis, 2000, lambda x: None)

    def BoidTrackbars(self):
        self.boidTrackball_name = "Boid-" + self.name
        cv2.namedWindow(self.boidTrackball_name)

        cv2.createTrackbar('size', self.boidTrackball_name, 10, int((self.width + self.height) / 2),
                           lambda x: None)

        cv2.createTrackbar('ali_dis', self.boidTrackball_name, 60,
                           int((self.width + self.height) / 2), lambda x: None)
        cv2.createTrackbar('sep_dis', self.boidTrackball_name, 30,
                           int((self.width + self.height) / 2), lambda x: None)
        cv2.createTrackbar('coh_dis', self.boidTrackball_name, 120,
                           int((self.width + self.height) / 2), lambda x: None)

        cv2.createTrackbar('ali_bias', self.boidTrackball_name, 9, 100, lambda x: None)
        cv2.createTrackbar('sep_bias', self.boidTrackball_name, 25, 100, lambda x: None)
        cv2.createTrackbar('coh_bias', self.boidTrackball_name, 4, 100, lambda x: None)

        cv2.createTrackbar('maxSpeed', self.boidTrackball_name, 6,
                           int(max(self.width, self.height)), lambda x: None)
        cv2.createTrackbar('maxForce', self.boidTrackball_name, 50, 1000, lambda x: None)

        cv2.createTrackbar('add Boid', self.boidTrackball_name, 0, 1, lambda x: self.addRndBoid())

    def addBoid(self, boid):
        self.boids.append(boid)

    def addBoids(self, boids):
        self.boids += boids

    def addPredator(self, pred):
        self.predators.append(pred)

    def addPredators(self, predators):
        self.predators += predators

    def getRndPos(self):
        x = np.random.randint(0, self.width)
        y = np.random.randint(0, self.height)
        return Vector(x, y)

    def addRndBoid(self):
        pos = self.getRndPos()
        boid = Boid(pos.x, pos.y, self)
        self.addBoid(boid)

    def addRndBoids(self, num):
        for i in range(num):
            self.addRndBoid()

    def addRndPredator(self):
        pos = self.getRndPos()
        pred = Predator(pos.x, pos.y, self)
        self.predators.append(pred)

    def addRndPredators(self, num):
        for i in range(num):
            self.addRndPredator()

    def addMousePredator(self):
        m_pred = MousePredator(self)
        self.predators.append(m_pred)
        
     
