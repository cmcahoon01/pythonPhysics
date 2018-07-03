from graphics import *
import time
import random

grav = 100
drag = 1
friction = 0.95


class Ball(Circle):

    def __init__(self, pt, r, w, bs):
        Circle.__init__(self, pt, r)
        self.window = w
        self.xSpeed = 0
        self.ySpeed = (250 - self.getCenter().getX()) * 4 / 100
        self.balls = bs
        self.gravity = -0 * self.getRadius()

    def changeSpeed(self, dx, dy):
        self.xSpeed += dx
        self.ySpeed += dy

    def calcForces(self):
        yForce = self.gravity
        xForce = 0
        squish = 2
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
                    self.drag(friction)

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


def main():
    win = GraphWin("My Window", 500, 500)
    win.setBackground(color_rgb(255, 255, 255))
    balls = list()
    # for i in range(20):
    #     ran = (random.random()+1)*(win.getWidth()/2)
    #     balls.append(Ball(Point(ran, ran), ran/10, win, balls))
    balls.append(Ball(Point(150, 250), 10, win, balls))
    balls.append(Ball(Point(250, 250), 50, win, balls))
    balls.append(Ball(Point(340, 250), 15, win, balls))
    for ball in balls:
        ball.setFill(color_rgb(0, 0, 255))
        ball.setOutline(color_rgb(0, 0, 255))
        ball.draw(win)
    for i in range(10000):
        for ball in balls:
            if i % 800 == 0:
                ball.gravity *= -1
            ball.calcForces()
        for ball in balls:
            ball.step()
        time.sleep(0.005)
    win.close()


main()
