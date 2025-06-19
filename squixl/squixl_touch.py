import asyncio

from SQUiXL import touch

class _SQ_Touch():	
	def __init__(self):	
		self.touch = touch
		self.point = -1,-1
		asyncio.create_task(self.check())
		self.targets = []
	
	def __call__(self,rectangle,action):
		x,y,width,height = rectangle
		box = x,x+width,y,y+height
		self.targets.append((box,action))
	
	async def check(self):
		last_y = last_x = -1
		while True:
			points = self.touch.read_points()[1]
			if (last_y != points[0][0]) and (last_x != points[0][1]):
				point = points[0][1],points[0][0]
				await self.check_targets(point)
				last_x = points[0][1]
				last_y = points[0][0]
			await asyncio.sleep(0.3)
	
	async def check_targets(self,point):
		x,y = point
		for target in self.targets:
			x_min,x_max,y_min,y_max = target[0]
			if (x > x_min) and (x < x_max) and (y > y_min) and (y < y_max):
				await target[1]()
				break
'''				
create a singleton instance of SQ_Touch that acts
as a function to add new targets
'''				
def active_targets():
	add_target =_SQ_Touch()
	def get():
		nonlocal add_target
		return add_target	
	return get
	
get_add_target = active_targets()
