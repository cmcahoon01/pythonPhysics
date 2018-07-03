from graphics import *
import time
import random

speed = int(input())

grav = 100
drag = 1
friction = 0.99
squish = 2
fall = 0



class Ball(Circle):
    def __init__(self, pt, r, w, bs, yS=0, xS=0):
        Circle.__init__(self, pt, r)
        self.window = w
        self.xSpeed = xS
        self.ySpeed = yS
        self.balls = bs
        self.gravity = fall * self.getRadius()

    def changeSpeed(self, dx, dy):
        self.xSpeed += dx
        self.ySpeed += dy

    def calcForces(self):
        yForce = self.gravity
        xForce = 0

        if self.getCenter().getY() + self.getRadius() > self.window.getHeight():
            yForce += (self.window.getHeight() - (self.getCenter().getY() + self.getRadius())) * squish
            self.drag(friction)
        elif self.getCenter().getY() - self.getRadius() < 0:
            yForce += -(self.getCenter().getY() - self.getRadius()) * squish
            self.drag(friction)
        if self.getCenter().getX() + self.getRadius() > self.window.getWidth():
            xForce += (self.window.getWidth() - (self.getCenter().getX() + self.getRadius())) * squish
            self.drag(friction)
        elif self.getCenter().getX() - self.getRadius() < 0:
            xForce += -(self.getCenter().getX() - self.getRadius()) * squish
            self.drag(friction)

        for ball in self.balls:
            if ball is not self:
                dist = distance(ball.getCenter(), self.getCenter())
                if grav > 0:
                    intensity = grav / dist
                    yddt = abs(ball.getCenter().getY() - self.getCenter().getY()) / dist * intensity
                    if ball.getCenter().getY() < self.getCenter().getY():
                        yddt *= -1
                    yForce += yddt
                    xddt = abs(ball.getCenter().getX() - self.getCenter().getX()) / dist * intensity
                    if ball.getCenter().getX() < self.getCenter().getX():
                        xddt *= -1
                    xForce += xddt

                if dist <= ball.getRadius() + self.getRadius():
                    intensity = ((ball.getRadius() + self.getRadius()) - dist) * squish
                    yddt = abs(ball.getCenter().getY() - self.getCenter().getY()) / dist * intensity
                    if ball.getCenter().getY() > self.getCenter().getY():
                        yddt *= -1
                    yForce += yddt
                    xddt = abs(ball.getCenter().getX() - self.getCenter().getX()) / dist * intensity
                    if ball.getCenter().getX() > self.getCenter().getX():
                        xddt *= -1
                    xForce += xddt
                    yForce += ball.ySpeed - self.ySpeed
                    xForce += ball.xSpeed - self.xSpeed

        self.ySpeed += yForce / self.getRadius()
        self.xSpeed += xForce / self.getRadius()
        self.drag(drag)

    def drag(self, d):
        self.ySpeed *= d
        self.xSpeed *= d

    def step(self):
        self.move(self.xSpeed, self.ySpeed)


def distance(p1, p2):
    return ((p1.getX() - p2.getX()) ** 2 + (p1.getY() - p2.getY()) ** 2) ** (1 / 2)


def bounce():
    global grav
    global drag
    global friction
    global squish
    global fall
    grav = 0
    drag = 0.99
    friction = 0.95
    squish = 5
    fall = -0.1
    win = GraphWin("Bouncy", 500, 500)
    win.setBackground(color_rgb(255, 255, 255))
    balls = list()
    random.seed(3)
    for i in range(15):
        ran = (random.random() + 0.5) * (win.getWidth() / 1.5)
        balls.append(Ball(Point(ran, ran), ran / 10, win, balls))
    for ball in balls:
        ball.setFill(color_rgb(0, 0, 255))
        ball.setOutline(color_rgb(0, 0, 255))
        ball.draw(win)
    for i in range(2000):
        for ball in balls:
            if i % 500 == 0:
                ball.gravity *= -1
            ball.calcForces()
        for ball in balls:
            ball.step()
        time.sleep(0.005*speed)
    win.close()


def orbit():
    win = GraphWin("Orbit", 500, 500)
    win.setBackground(color_rgb(255, 255, 255))
    balls = list()
    balls.append(Ball(Point(150, 250), 10, win, balls, 4, 0))
    balls.append(Ball(Point(250, 250), 50, win, balls, 0, 0))
    balls.append(Ball(Point(340, 250), 15, win, balls, -3.6, 0))
    for ball in balls:
        ball.setFill(color_rgb(0, 0, 255))
        ball.setOutline(color_rgb(0, 0, 255))
        ball.draw(win)
    for i in range(1500):
        for ball in balls:
            if i % 500 == 0:
                ball.gravity *= -1
            ball.calcForces()
        for ball in balls:
            ball.step()
        time.sleep(0.008*speed)
    win.close()


orbit()
bounce()

