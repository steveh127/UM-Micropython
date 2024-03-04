'''
Plays random tracks from sd card

'''
import asyncio
from machine import Pin,reset
from random import randint
from console import Console
from wav_tools import WAV_Tools
	
class PlayRandom(WAV_Tools,Console):
	
	def __init__(self):
		WAV_Tools.__init__(self)
		Console.__init__(self)
		self.tracks = self.get_tracks(path='/sd/Music',with_paths=True)
	
	def get_random_track(self):
		i=randint(0,len(self.tracks) - 1)
		self.path,track=self.tracks[i]
		return track
		
	async def new_track(self):
		print('new_track')
		self.stop=True
		self.track=None
		await self.display.show('{RED}Wait')
		await asyncio.sleep(1)
		
	async def restart_now(self):
		print('Restarting')
		#await self.display_text('Restarting',1)
		await asyncio.sleep(0.2)
		reset()	
				
	async def set_volume(self):
		if self.track:
			self.set_vol = True
		await asyncio.sleep(0.3)
			
	async def run(self):
		asyncio.create_task(self())
		self.buttons[0].action=self.new_track
		self.buttons[1].action=self.mute_now
		await self.console_tasks()
		await self.display.show('Random')
		self.buttons[2].action=self.set_volume
		while True:
			if self.track is None:
				rt = self.get_random_track()
				if rt is None:
					break
				else:
					pass
					await self.display.show('{BLUE}' + rt + '  ')
				self.track = rt
				await asyncio.sleep(5)
			await asyncio.sleep(1)

play_random=PlayRandom()

asyncio.run(play_random.run())

