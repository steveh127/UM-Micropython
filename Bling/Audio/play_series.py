import asyncio
import os
from play_wav import Play_WAV
from console import Console

class PlaySeries(Play_WAV,Console):
	def __init__(self):
		Play_WAV.__init__(self)
		Console.__init__(self)
		self.title=os.listdir('/sd/audio')[0]
		self.episodes=os.listdir('/sd/audio/' + self.title)
		self.episodes.sort()
		try:
			with open('/sd/next_episode','rb') as nep:
				self.nxt=int(nep.read())
		except:
			with open('/sd/next_episode','wb') as nep:
				nep.write('0')
			self.nxt=0
		self.play_next=False
		self.skip=False
		self.back=False
		
	async def play_next_episode(self):
		while True:
			if self.play_next:
				self.play_next=False
				with open('/sd/next_episode','rb') as nep:
						self.nxt=int(nep.read())
						print(self.nxt)
				self.buttons[0].action=self.skip_episode
				self.buttons[1].action=self.previous_episode
				await self.display.show(self.title)	
				#await self.display_text('Skip   Vol  Back',3)
				parts=os.listdir('/sd/audio/' + self.title + '/' + self.episodes[self.nxt])
				self.path='/sd/audio/' + self.title + '/' + self.episodes[self.nxt] + '/'
				await self.display.show('{BLUE}' + self.episodes[self.nxt] + '  ')
				print('Episode: ' + self.episodes[self.nxt])
				for p in parts:
					if self.skip:
						self.skip = False
						await self.display.show(self.episodes[self.nxt+1])
						break
					if self.back:
						self.back = False
						await self.display.show(self.episodes[self.nxt-1])
						self.nxt -= 2
						break
					self.track=p[:-4]
					while self.track:
						if self.skip or self.back:
							self.stop = True
							break
						await asyncio.sleep(0)
				self.nxt += 1
				if self.nxt < 0:
					self.nxt = 0	
				if self.nxt == len(self.episodes):
					print('Series complete: Resetting to first episode')
					#await self.display_text('Reset to start',1)
					self.nxt = 0
				with open('/sd/next_episode','wb') as nep:
					nep.write(str(self.nxt))
				#await self.display_text('Start      Start',3)
				self.buttons[1].action=self.start_next
				self.buttons[0].action=self.start_next
			await asyncio.sleep(0)
			
	async def start_next(self):
		self.play_next = True
	
	async def set_volume(self):
		if self.track:
			self.set_vol = True
		await asyncio.sleep(0.3)
	
	async def skip_episode(self):
		self.skip = True
		await asyncio.sleep(0.3)
	
	async def previous_episode(self):
		self.back = True
		await asyncio.sleep(0.3)
	
	async def run(self):
		print(self.title)
		asyncio.create_task(self())
		asyncio.create_task(self.play_next_episode())
		await self.console_tasks()	
		await self.display.show(self.title)
		#await self.display_text('Start          ',3)
		self.buttons[0].action=self.start_next
		self.buttons[2].action=self.set_volume
		while True:
			await asyncio.sleep(10)

play_series=PlaySeries()
	 
asyncio.run(play_series.run())
