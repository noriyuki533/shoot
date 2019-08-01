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
        self.hp = 0
        self.color = 0
    
    def init(self, x=0, y=0, vx=0, vy=0, size=6, color=0, hp=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.hp = hp

    def selfDraw(self, color):
        rs = self.size
        pyxel.rect(self.x-rs/2, self.y-rs/2, self.x+rs/2, self.y+rs/2, self.color)

    def isOutside(self):
        return (self.y < 0) or (self.y > WINDOW_H)
    
    def hurt(self):
        self.hp -= 1
        if self.hp < 0:
            self.dead()
    
    def dead(self):
        self.alive = False

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        super().init(y=20, vx=3, vy=2, color=11, hp=50)
    
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

class Particle(GameObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 2
    
    def init(self, x, y, deg, speed, palette):
        super().init(x, y, deg, speed)
        self.palette = palette
        self.timer = 0

    def update(self):
        self.vx *= 0.97
        self.vy *= 0.97
        self.timer += 1
        if self.timer > 60:
            self.hurt()
    
    def dead(self):
        pass

    def draw(self):
        self.selfDraw(self.palette)

def isCollision(obj1: GameObject, obj2: GameObject):
    r1, r2 = obj1.size/2, obj2.size/2
    dx = abs(obj1.x - obj2.x)
    dy = abs(obj1.y - obj2.y)
    return dx < (r1 + r2) and dy < (r1 + r2)

class App:
    def __init__(self):
        pyxel.init(WINDOW_H, WINDOW_W, caption="SHOOT")
        self.player = Player()
        self.enemy = Enemy()
        self.Bullets = []
        self.Particles = []

        #run after all initialization
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.player.alive:
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
        for i, bullet in enumerate(self.Bullets):
            bullet.update()

            if bullet.isOutside():
                #print(bullet.isOutside())
                del self.Bullets[i]

            if isCollision(bullet, self.player):
                self.player.alive = False
            
            if isCollision(bullet, self.enemy):
                self.enemy.hurt()
                del self.Bullets[i]
                self.Particles.append(Particle())
        
        for i, particle in enumerate(self.Particles):
            particle.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(WINDOW_W/2-5, 10, "SHOOT", pyxel.frame_count//5 % 3 + 7)
        pyxel.text(5, 10, "HP:{}".format(self.enemy.hp), 7)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)

        if not self.player.alive:
            pyxel.text(WINDOW_W/2-20, 100, "GAME OVER", pyxel.frame_count//5 % 3 + 2)
        else:
            self.player.selfDraw(11)
        
        self.enemy.selfDraw(14)

        for i, bullet in enumerate(self.Bullets):
            bullet.selfDraw(9)
        for i, particle in enumerate(self.Particles):
            particle.selfDraw(8)
        
App()