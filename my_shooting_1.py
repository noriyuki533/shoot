import pyxel
import math
import random

WINDOW_H = 200
WINDOW_W = 200

class GameObject:
    def __init__(self):
        self.x = 0
        self.y = 10
        self.vx = 2
        self.vy = 0
        self.size = 6
        self.alive = True

    def selfDraw(self, color):
        if not self.alive:
            return

        rs = self.size
        pyxel.rect(self.x-rs/2, self.y-rs/2, self.x+rs/2, self.y+rs/2, color)

    def isOutside(self):
        return (self.x < 0 or self.x > WINDOW_W) or (self.y < 0 or self.y > WINDOW_H)

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 10
        self.vx = 2
        self.vy = 0
        self.size = 6
    
    def update(self):
        xn = self.x + self.vx
        if xn > WINDOW_W or xn < 0:
            self.vx *= -1
        
        self.x += self.vx

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.size = 5
    
    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y

class Bullet(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = -3
        self.size = 3

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.isOutside():
            self.alive = False

    def setSpeed(self, speed):
        self.vx = self.vy = speed

class App:
    def __init__(self):
        pyxel.init(WINDOW_H, WINDOW_W, caption="SHOOT")
        self.player = Player()
        self.enemy = Enemy()
        self.Bullets = []

        #run after all initialization
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            new_bullet = Bullet()
            new_bullet.x = pyxel.mouse_x
            new_bullet.y = pyxel.mouse_y
            self.Bullets.append(new_bullet)

        
        self.player.update()
        self.enemy.update()
        for bullet in self.Bullets:
            bullet.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(WINDOW_W/2-5, 10, "SHOOT", pyxel.frame_count//5 % 3 + 7)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)

        self.player.selfDraw(11)
        self.enemy.selfDraw(14)

        for bullet in self.Bullets:
            bullet.selfDraw(9)

App()