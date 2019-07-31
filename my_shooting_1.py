import pyxel
import math
import random

WINDOW_H = 200
WINDOW_W = 200

class GameObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.size = 6
        self.alive = True
        self.color = 0
    
    def init(self, x=0, y=0, vx=0, vy=0, size=6, color=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color

    def selfDraw(self, color):
        rs = self.size
        pyxel.rect(self.x-rs/2, self.y-rs/2, self.x+rs/2, self.y+rs/2, self.color)

    def isOutside(self):
        return (self.y < 0) or (self.y > WINDOW_H)

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        super().init(y=20, vx=3, vy=2, color=11)
    
    def update(self):
        xn = self.x + self.vx
        if xn > WINDOW_W or xn < 0:
            self.vx *= -1
        
        yn = self.y + self.vy
        if yn > 40 or yn < 10+self.size:
            self.vy *= -1
        
        self.x += self.vx
        self.y += self.vy

class Player(GameObject):
    def __init__(self):
        super().__init__()
        super().init(size=6, color=10)
    
    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y

class Bullet(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = -5
        self.size = 3
        self.color = 9

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
            #print(len(self.Bullets))
        
        if pyxel.frame_count % random.randint(1,10) == random.randint(0,10):
            new_bullet = Bullet()
            new_bullet.init(x=self.enemy.x, y=self.enemy.y, vy=7, size=4, color=8)
            self.Bullets.append(new_bullet)

        
        self.player.update()
        self.enemy.update()
        for bullet in self.Bullets:
            bullet.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(WINDOW_W/2-5, 10, "SHOOT", pyxel.frame_count//5 % 3 + 7)
        pyxel.text(5, 10, str(len(self.Bullets)), 7)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)

        self.player.selfDraw(11)
        self.enemy.selfDraw(14)

        for i, bullet in enumerate(self.Bullets):
            if bullet.isOutside():
                #print(bullet.isOutside())
                del self.Bullets[i]
            else:
                bullet.selfDraw(9)

App()