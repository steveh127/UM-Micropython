'''
Music on sd card must be in:

artist/album/tracks format

console required to select tracks.

tested on teensy audio and with wav master
for wav master L button - next / skip, R button pick, both together voloume 

'''
import asyncio
import os
from wav_tools import WAV_Tools
from console import Console

class Play_Tools(WAV_Tools,Console):
	def __init__(self):
		WAV_Tools.__init__(self)
		Console.__init__(self)
		#random
		self.tracks = self.get_tracks(path='/sd/Music',with_paths=True)
		#albums
		self.artists=self.get_dirs(path='/sd/Music')
		self.album=None
		self.next=False
		self.pick=False
		self.artist=None
		#series
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
		
	async def play_album(self):
		while True:
			if self.album is not None:
				await self.display.show(self.album + '  ' + self.artist + '  ')
				#await self.display_text('Skip   Vol  Mute',3)			
				tracks = self.get_tracks(path='/sd/Music' + '/' + self.artist + '/' + self.album)
				for tr in tracks:
					self.track = tr
					await self.display.show(self.track)
					while self.track:
						if self.next:
							self.stop=True
							self.next=False
						if self.pick:
							self.pick=False
							await self.mute_now()
						await asyncio.sleep(0)
				self.album = None
			else:
				await asyncio.sleep(1)
	
	async def select_album(self):
		while True:
			if self.album is None:
				await self.display.show('Select Artist')
				while not self.pick:
					for artist in self.artists:
						await self.display.show(artist) 
						while not self.next and not self.pick:
							await asyncio.sleep(0)
						if self.pick:
							self.artist=artist
							break	
						self.next=False
				self.pick=False
				print(self.artist + ' selected')
				albums=self.get_dirs('/sd/music/' + self.artist)
				if len(albums)==1:
					self.album=albums[0]
					await self.display.show(self.album)
				else:
					await self.display.show('Select Album ')
					while not self.pick:
						for album in albums:
							await self.display.show(album)
							while not self.next and not self.pick:
								await asyncio.sleep(0)
							if self.pick:
								self.album=album
								break	
							self.next=False
				self.pick=False		
			await asyncio.sleep(1)	
			
	async def get_next(self):
		self.next=True
		await asyncio.sleep(0.3)
		
	async def picked(self):
		self.pick=True
		await asyncio.sleep(0.3)
			
	async def set_volume(self):
		if self.track:
			self.set_vol=True
		await asyncio.sleep(0.3)		
					
	async def run(self):
		asyncio.create_task(self())
		asyncio.create_task(self.play_album())
		asyncio.create_task(self.select_album())
		await self.console_tasks()
		self.buttons[0].action=self.get_next
		self.buttons[1].action=self.picked
		self.buttons[2].action=self.set_volume
		while True:
			await asyncio.sleep(10)
			
play_albums=Play_Tools()
asyncio.run(play_albums.run())
