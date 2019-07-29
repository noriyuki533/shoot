import pyxel
import math
import random
 
# ゲームオブジェクト
class GameObject:
	def __init__(self):
		self.exists = False
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
		self.size = 6
		self.hp = 1
	def init(self, x, y, deg, speed):
		self.x, self.y = x, y
		rad = math.radians(deg)
		self.setSpeed(rad, speed)
	def move(self):
		self.x += self.vx
		self.y += self.vy
	def setSpeed(self, rad, speed):
		self.vx, self.vy = speed * math.cos(rad), speed * -math.sin(rad)
	def drawSelf(self, palette):
		r2 = self.size/2
		pyxel.rect(self.x-r2, self.y-r2, self.x+r2, self.y+r2, palette)
	def isOutSide(self):
		r2 = self.size/2
		return self.x < -r2 or self.y < -r2 or self.x > pyxel.width+r2 or self.y > pyxel.height+r2
	def clipScreen(self):
		r2 = self.size/2
		self.x = r2 if self.x < r2 else self.x
		self.y = r2 if self.y < r2 else self.y
		self.x = pyxel.width-r2 if self.x > pyxel.width-r2 else self.x
		self.y = pyxel.height-r2 if self.y > pyxel.height-r2 else self.y
	def update(self):
		self.move()
		if self.isOutSide():
			self.exists = False
	def dead(self):
		pass
	def hurt(self, val=1):
		if self.exists == False:
			return
		self.hp -= val
		if self.hp <= 0:
			self.exists = False
			self.dead()
 
# ゲームオブジェクト管理
class GameObjectManager:
	def __init__(self, num, obj):
		self.pool = []
		for i in range(0, num):
			self.pool.append(obj())
	def add(self):
		for obj in self.pool:
			if obj.exists == False:
				obj.exists = True
				return obj
		return None
	def update(self):
		for obj in self.pool:
			if obj.exists:
				obj.update()
	def draw(self):
		for obj in self.pool:
			if obj.exists:
				obj.draw()
	def vanish(self):
		for obj in self.pool:
			if obj.exists:
				obj.hurt(999)
 
# 自機
class Player(GameObject):
	def __init__(self):
		super().__init__()
		self.x = pyxel.width/2
		self.y = pyxel.height*5/6
		self.size = 6
		self.exists = True
	def update(self):
		if self.exists == False:
			return
		
		if pyxel.btnp(pyxel.KEY_SPACE):
			Shot.add(self.x, self.y, 90, 5) # 弾を撃つ
		
		# Moving...
		dx, dy = 0, 0
		if pyxel.btn(pyxel.KEY_LEFT):
				dx = -1
		elif pyxel.btn(pyxel.KEY_RIGHT):
				dx = 1
		if pyxel.btn(pyxel.KEY_UP):
				dy = -1
		elif pyxel.btn(pyxel.KEY_DOWN):
				dy = 1
		if(dx == 0 and dy == 0):
			return # 動いていない
		rad = math.atan2(-dy, dx)
		speed = 2
		self.setSpeed(rad, speed)
		self.move()
		self.clipScreen()
	def dead(self):
		for i in range(32):
			deg = random.randrange(0, 360);
			speed = 0.1 + random.random() * 1.5
			Particle.add(self.x, self.y, deg, speed, 7)
	def draw(self):
		if self.exists == False:
			return
		self.drawSelf(7)
 
# 自弾
class Shot(GameObject):
	mgr = None
	@classmethod
	def add(cls, x, y, deg, speed):
		obj = cls.mgr.add()
		if obj != None:
			obj.init(x, y, deg, speed)
	def __init__(self):
		super().__init__()
		self.size = 4
		self.exists = False
	def dead(self):
		pass
	def draw(self):
		self.drawSelf(6)
 
# 敵
class Enemy(GameObject):
	mgr = None
	target = None
	loop = 0
	@classmethod
	def add(cls, eid, x, y, deg, speed):
		obj = cls.mgr.add()
		if obj != None:
			obj.init(eid, x, y, deg, speed)
	def __init__(self):
		super().__init__()
		self.size = 12
		self.exists = False
	def init(self, eid, x, y, deg, speed):
		super().init(x, y, deg, speed)
		self.timer = 0
		self.eid = eid
		
		# データ定義
		dataTbl = [
		# hp, size, destroy
			[],
			[5, 12, 240, self.update1], # eid:1
			[1, 6, 240, self.update2], # eid:2
			[2, 4, 480, self.update3], # eid:3
			[5, 12, 240, self.update4], # eid:4
			[5, 12, 480, self.update5], # eid:5
			[5, 12, 240, self.update6], # eid:6
		]
		data = dataTbl[eid]
		self.hp = data[0]
		self.size = data[1]
		self.tDestroy = data[2]
		self.func = data[3]
		self.aim = 0
	def getAim(self):
		dx = self.target.x - self.x
		dy = self.target.y - self.y
		return math.degrees(math.atan2(-dy, dx))
	def bullet(self, deg, speed):
		# 弾を撃つ
		speed += Enemy.loop * 0.5 # ループするほど敵弾の速度が上がる
		Bullet.add(self.x, self.y, deg, speed)
	def bulletAim(self, ofs, speed):
		# 狙い撃ち弾
		aim = self.getAim()
		self.bullet(aim+ofs, speed)
	def dead(self):
		for i in range(8):
			deg = random.randrange(0, 360);
			speed = 1
			Particle.add(self.x, self.y, deg, speed, 11)
	def update(self):
		super().update()
		self.func()
		
		self.timer += 1
		if self.timer >= self.tDestroy:
			# 自爆
			self.hurt(999)
	def update1(self):
		self.vx *= 0.95
		self.vy *= 0.95
		for i in range(5):
			if self.timer%60 == (i*3)+40:
				if i == 0:
					self.aim = self.getAim()
				self.bullet(self.aim, 4)
	def update2(self):
		self.vx *= 0.97
		self.vy *= 0.97
		t = self.timer%120
		if t == 60 or t == 80 or t == 100:
#			for i in range(3):
			for i in range(1):
				aim = self.getAim() - 2 + 2*i
				self.bullet(aim, 0.5)
	def update3(self):
		self.vx *= 0.97
		self.vy *= 0.97
		if self.timer < 60:
			return
		if self.timer%75 == 0:
			self.bulletAim(0, 4)
	def update4(self):
		self.vx *= 0.95
		self.vy *= 0.95
		if self.timer < 60:
			return
		ofs = 20 * math.sin(math.radians(self.timer*2))
		self.bullet(270+ofs, 5)
	def update5(self):
		self.vx *= 0.95
		self.vy *= 0.95
		if self.timer < 60:
			return
		for i in range(10):
			if self.timer%60 == (i*3):
				if i == 0:
					self.aim = self.getAim()
				for i in range(3):
					self.bullet(self.aim-25+25*i, 3)
	def update6(self):
		self.vx *= 0.95
		self.vy *= 0.95
		if self.timer < 60:
			return
		self.bullet(120 + self.timer*7, 2)
	def draw(self):
		self.drawSelf(11)
 
# 敵弾
class Bullet(GameObject):
	mgr = None
	@classmethod
	def add(cls, x, y, deg, speed):
		obj = cls.mgr.add()
		if obj != None:
			obj.init(x, y, deg, speed)
	def __init__(self):
		super().__init__()
		self.size = 4
	def dead(self):
		pass
	def draw(self):
		self.drawSelf(8)
 
# パーティクル
class Particle(GameObject):
	mgr = None
	@classmethod
	def add(cls, x, y, deg, speed, palette):
		obj = cls.mgr.add()
		if obj != None:
			obj.init(x, y, deg, speed, palette)
	def __init__(self):
		super().__init__()
		self.size = 1
	def init(self, x, y, deg, speed, palette):
		super().init(x, y, deg, speed)
		self.palette = palette
		self.timer = 0
	def update(self):
		super().update()
		self.vx *= 0.97
		self.vy *= 0.97
		self.timer += 1
		if self.timer > 60:
			self.hurt(999)
	def dead(self):
		pass
	def draw(self):
		self.drawSelf(self.palette)
 
# ボス
class Boss(GameObject):
	def __init__(self):
		super().__init__()
		self.size = 32
		self.timer = 0
		self.init(pyxel.width/2, 30, 0, 0)
		self.exists = True
		self.hp = 75
	def spawn(self, eid, deg, speed):
		Enemy.add(eid, self.x, self.y, deg, speed)
	def update(self):
		if self.exists == False:
			return;
		self.timer += 1
		t = self.timer
		if t == 60:
			self.spawn(1, 225, 2)
			self.spawn(1, 315, 2)
		if t%240 == 150:
			self.spawn(2, random.randrange(0, 360), 1)
		if t == 300:
			for i in range(20):
				self.spawn(3, i * 360/20, 1);
		if t == 440:
			self.spawn(4, 0, 2)
			self.spawn(4, 180, 2)
		if t == 600:
			self.spawn(5, 15, 2)
			self.spawn(5, 165, 2)
		if t == 760:
			self.spawn(6, 30, 2)
			self.spawn(6, 210, 2)
		if t == 900:
			# 最初に戻る
			self.timer = 0
			Enemy.loop += 1 # ループ回数をカウントアップ
	def dead(self):
		for i in range(32):
			deg = random.randrange(0, 360);
			speed = 0.1 + random.random() * 1.5
			Particle.add(self.x, self.y, deg, speed, 9)
	def draw(self):
		if self.exists == False:
			return;
		pyxel.text(self.x+24, self.y, "HP:%d"%self.hp, 7)
		self.drawSelf(9)
 
# 衝突判定
def overlaped(obj1, obj2):
	r1, r2 = obj1.size/2, obj2.size/2
	dx = abs(obj1.x - obj2.x)
	dy = abs(obj1.y - obj2.y)
	return dx < (r1 + r2) and dy < (r1 + r2)
 
class App:
	def __init__(self):
		pyxel.init(160, 240, caption="Test", fps=60)
		self.init()
		pyxel.run(self.update, self.draw)
		
	def init(self):
		self.player = Player()
		Shot.mgr = GameObjectManager(32, Shot)
		Enemy.mgr = GameObjectManager(32, Enemy)
		Enemy.target = self.player
		self.boss = Boss()
		Bullet.mgr = GameObjectManager(256, Bullet)
		Particle.mgr = GameObjectManager(256, Particle)
		Enemy.loop = 0
		
	def update(self):
		if pyxel.btnp(pyxel.KEY_1):
			pyxel.quit()
		if pyxel.btnp(pyxel.KEY_R):
			self.init()
			
		# 各種オブジェクトの更新
		self.player.update()
		Shot.mgr.update()
		Enemy.mgr.update()
		self.boss.update()
		Bullet.mgr.update()
		Particle.mgr.update()
		
		if self.boss.exists == False:
			return
		
		# 自弾と敵との当たり判定
		for s in Shot.mgr.pool:
			if s.exists == False:
				continue
			
			for e in Enemy.mgr.pool:
				if e.exists == False:
					continue
				if overlaped(s, e):
					s.hurt()
					e.hurt()
					break
			
			if overlaped(s, self.boss):
				s.hurt()
				self.boss.hurt()
				if self.boss.exists == False:
					# 敵と敵弾を全て消す
					Enemy.mgr.vanish()
					Bullet.mgr.vanish()
		# 自機と敵弾との当たり判定
		if self.boss.exists == True:
			for b in Bullet.mgr.pool:
				if overlaped(self.player, b):
					self.player.hurt()
	def draw(self):
		pyxel.cls(0)
		self.player.draw()
		Shot.mgr.draw()
		Enemy.mgr.draw()
		self.boss.draw()
		Bullet.mgr.draw()
		Particle.mgr.draw()
 
		if self.player.exists == False:
			pyxel.text(64, 100, "GAME OVER", 7)
			pyxel.text(48, 120, "Press 'R' to Restart", 7)
			
		if self.boss.exists == False:
			pyxel.text(48, 100, "MISSIN COMPLETE", 7)
			pyxel.text(40, 120, "Congratulations!!!", 7)
App()