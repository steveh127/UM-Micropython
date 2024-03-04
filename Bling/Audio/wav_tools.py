import asyncio
import os
from random import randint

from play_wav import Play_WAV

class WAV_Tools(Play_WAV):
	def __init__(self):
		super().__init__()
		self.tracks=[]
	
#recursively finds all tracks on SD 	
	def get_tracks(self,path='/sd/',*,tracks=None,album=None,with_paths=False,root=False):
		wp=with_paths
		if album is not None:
			self.path = path + '/' + album
		else:
			self.path=path
		if tracks is None:
			tracks=[]
		else:
			tracks=tracks	
		dirs=[]
		for ft in os.ilistdir(self.path):
			f,typ,_,_ = ft
			if '.wav' in f:
				if with_paths:
					tracks.append((self.path,f[:-4]))
				else:
					tracks.append(f[:-4])
			if typ == 16384:
				dirs.append(f)
		for d in dirs:
			tracks=self.get_tracks(path=path + '/' + d,tracks=tracks,with_paths=wp)
		return tracks
	
	def get_albums(self):
		albums=[]
		files=os.listdir('/sd')
		for f in files:
			if '.' not in f:
				albums.append(f)
		return albums
	
	def get_dirs(self,path='/sd'):
		dirs=[]
		files=os.listdir(path)
		for f in files:
			if '.' not in f:
				dirs.append(f)
		return dirs
			
