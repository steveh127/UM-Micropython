import asyncio

from SQUiXL import touch

class SQ_Touch():
	def __init__(self):
		self.touch = touch
		self.touched = False
		self.point = -1,-1
		self.targets = []
		asyncio.create_task(self.check())
		
	def add_target(self,rectangle,action):
		x,y,width,height = rectangle
		box = x,x+width,y,y+height
		self.targets.append((box,action))

	async def check(self):
		last_y = last_x = -1
		while True:
			points = self.touch.read_points()[1]
			if last_y != points[0][0] and last_x != points[0][1]:
				point = points[0][1],points[0][0]
				self.check_targets(point)
				last_x = points[0][1]
				last_y = points[0][0]
			await asyncio.sleep(0.1)
	
	def check_targets(self,point):
		for target in self.targets:
			x,y = point
			x_min,x_max,y_min,y_max = target[0]
			if (x > x_min) and (x < x_max) and (y > y_min) and (y < y_max):
				target[1]()
				break
