import pyxel
import math
import random

WINDOW_H = 200
WINDOW_W = 200

class Enemy:
    def __init__(self):
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

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 5
    
    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = -3
        self.size = 3

    def update(self):
        self.x += self.vx
        self.y += self.vy

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

        rs = self.player.size
        pyxel.rect(self.player.x-rs/2, self.player.y-rs/2, self.player.x+rs/2, self.player.y+rs/2, 11)

        rs = self.enemy.size
        pyxel.rect(self.enemy.x-rs/2, self.enemy.y-rs/2, self.enemy.x+rs/2, self.enemy.y+rs/2, 14)

        for bullet in self.Bullets:
            pyxel.circ(bullet.x, bullet.y, bullet.size, pyxel.frame_count % 16)

App()