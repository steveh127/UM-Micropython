'''
Program to display time on an 9 x 9 neopixel array
version for UM Crystal display using ESP32 S3

On first booting or on the boot following a failure to boot the
program launches 'weblink' to provide a web interface to set network
parameters. Clock settings can be set too. 

See README for detailed instructions.

Except for setup the clock only connects to the network on initial boot
and then twice a day to keep clock in sync using NTPtime.

weblink and web_builder are not the standard versions as they
are specialised to use access point for configuration.

'''

import asyncio
from machine import Pin, RTC, WDT
from neopixel import NeoPixel
import network
import ntptime
from random import randrange


from net_config import SSID,PSWD,SHAPE,H12,OFFSET
from colour_config import H10C,H1C,M10C,M1C,BRD,CRS,M1Z,M10Z,H1Z,H10Z,CNT

class Neo_time():
	def __init__(self,neo_pin):
		self.UTC_offset = OFFSET
		self.ds  = False
		self.H12 = H12
		
		#setup neopixels
		self.neo = NeoPixel(neo_pin,81)
		self.neo.fill((0,0,0))
		self.neo.write()
		#full screen map
		# self.screen =[
		# 00,01,02,03,04,05,06,07,08,
		# 09,10,11,12,13,14,15,16,17,
		# 18,19,20,21,22,23,24,25,26,
		# 27,28,29,30,31,32,33,34,35,
		# 36,37,38,39,40,41,42,43,44,
		# 45,46,47,48,49,50,51,52,53,
		# 54,55,56,57,58,59,60,61,62,
		# 63,64,65,66,67,68,69,70,71,
		# 72,73,74,75,76,77,78,79,80
		# ]
		#border
		self.border = [0,1,2,3,4,5,6,7,8,9,17,18,26,27,35,36,44,45,53,54,62,63,71,72,73,74,75,76,77,78,79,80]
		#cross
		self.cross  = [13,22,31,37,38,39,40,41,42,43,49,58,67]
		self.centre = 40
		self.shape = SHAPE
		#all but edges - fully random
		self.full = [14,15,16,23,24,25,32,33,34,50,51,52,59,60,61,68,69,70,
					 46,47,48,55,56,57,64,65,66,10,11,12,19,20,21,28,29,30,
					 13,22,31,37,38,39,40,41,42,43,49,58,67]
		#create RTC object and set default time
		self.rtc = RTC()
		self.rtc.datetime((2022,1,1,1,19,59,0,0)) #(year,month,day,day of week,hour,minute,second,subsecond)

	@property
	def shape(self):
		return self.__shape
	
	@shape.setter
	def shape(self,value):
		if value not in ('blocks','circles','random'):
			self.__shape = 'blocks'
		else:
			self.__shape = value
		if self.__shape == 'blocks':
			#led mapping for 9 x 9 neopixel array	
			self.H10 = [14,15,16,23,24,25,32,33,34]
			self.H1  = [50,51,52,59,60,61,68,69,70]
			self.M1  = [46,47,48,55,56,57,64,65,66]
			self.M10 = [10,11,12,19,20,21,28,29,30]
		if self.__shape == 'circles':
			self.H10 = [30,31,32,39,41,48,49,50]	
			self.H1  = [20,21,22,23,24,29,33,38,42,47,51,56,57,58,59,60]
			self.M10 = [10,11,12,13,14,15,16,19,25,28,34,37,43,46,52,55,61,64,65,66,67,68,69,70]
			self.M1  = self.border
		

	#shuffle elements of a list
	def _shuffle(self,l):
		n = len(l)
		for _ in range(n):
			a = randrange(n)
			b = randrange(n)
			(l[a],l[b])=(l[b],l[a])
			
	#sort out daylight saving - 4th Sunday in March & October		
	def _set_ds(self):
		(_,month,day,dow,_,_,_,_) = self.rtc.datetime()
		if month in [11,12,1,2,3]:
			self.ds = False
		if month in [4,5,6,7,8,9,10]:
			self.ds = True	
		if month == 3 and dow == 6 and day > 24:
			self.ds = True
		if month == 3 and (day + (6 - dow)) > 30:
			self.ds = True		
		if month == 10 and dow == 6 and day > 24:
			self.ds = False	
		if month == 10 and (day + (6 - dow)) > 30:
			self.ds = False
		
	async def set(self):
		#connect to network
		print('setting time')
		net = network.WLAN(network.STA_IF)
		net.active(True)
		net.config(reconnects=0)
		i=0
		while i < 100:
			i += 1
			try:
				net.connect(SSID,PSWD)
			except OSError as e:
				await asyncio.sleep(0.1)
			if net.isconnected():
				print('Connected') 
				break
		if i == 100:
			print('Not Connected') 
			net_config = open('net_config.py','w')
			net_config.write('SSID=\'\'\n')
			net_config.write('PSWD=\'\'\n')
			net_config.write('SHAPE=\'blocks\'\n')
			net_config.write('H12=False\n')
			net_config.write('OFFSET=0\n')
			net_config.close()
			self.neo.fill((0,0,1))
			self.neo.write()
			await asyncio.sleep(10)
			self.rtc.datetime((2022,1,1,1,0,0,0,0))
			return
		#set time from network
		NTP_SERVER = '0.ch.pool.ntp.org'
		ntptime.host = NTP_SERVER
		i = 0
		while i < 100:
			i += 1
			try:
				ntptime.settime()
				print('Time Set')
			except OSError as e:
				print(e)
				await asyncio.sleep(1)
			else:
				break
		#disconnect from network
		net.disconnect()
		self._set_ds()
	
	def _get_time(self):
		(yr,mnth,day,dow,hr,mnt,sec,_)=self.rtc.datetime()
		if self.UTC_offset:
			if self.UTC_offset > 0:
				hr += self.UTC_offset
				if hr > 24:
					hr -= 24
				if hr < 0:
					hr += 24
		#only consider daylight saving if no offset
		else:
			if self.ds:
				hr += 1
				if hr == 24:
					hr = 0
		if self.H12:
			if hr > 12:
				hr = hr - 12
			if hr == 0:
				hr = 12
		self.h10 = int(hr/10)
		self.h1  = hr - self.h10*10
		self.m10 = int(mnt/10)
		self.m1  = mnt - self.m10*10
		return sec
			
	async def show(self):
		wdt=WDT(timeout=5000)
		print(self.rtc.datetime())
		while True:
			wdt.feed()
			sec = self._get_time()
			if sec % 5 == 0:
				if self.shape in ('blocks','circles'):
					self.neo.fill((0,0,0))
					self._shuffle(self.H10)
					for n in range(self.h10):
						self.neo[self.H10[n]] = H10C
					self._shuffle(self.H1)
					for n in range(self.h1):
						self.neo[self.H1[n]]  = H1C	
					self._shuffle(self.M10)	
					for n in range(self.m10):
						self.neo[self.M10[n]] = M10C
					self._shuffle(self.M1)
					for n in range(self.m1):
						self.neo[self.M1[n]]  = M1C	
					if self.shape == 'blocks':
						for n in self.border:
							self.neo[n] = BRD	
						for n in self.cross:
							self.neo[n] = CRS
					if self.shape == 'circles':
						self.neo[self.centre] = CNT
						if self.m1 == 0:
							for i in self.M1:
								self.neo[i] = M1Z
						if self.m10 == 0:
							for i in self.M10:
								self.neo[i] = M10Z
						if self.h1 == 0:
							for i in self.H1:
								self.neo[i] = H1Z
						if self.h10 == 0:
							for i in self.H10:
								self.neo[i] = H10Z
				else:
					self.neo.fill((0,0,0))
					self._shuffle(self.full)
					i = 0
					for n in range(self.h10):
						self.neo[self.full[i]] = H10C
						i += 1
					for n in range(self.h1):
						self.neo[self.full[i]] = H1C	
						i += 1
					for n in range(self.m10):
						self.neo[self.full[i]] = M10C
						i += 1
					for n in range(self.m1):
						self.neo[self.full[i]] = M1C
						i += 1
					for n in self.border:
						self.neo[n] = BRD	
				self.neo.write()
				await asyncio.sleep(1)		

class Button():
	def __init__(self,button_pin):
		self.button = Pin(button_pin,Pin.IN,Pin.PULL_UP)
		self.pressed = False
		asyncio.create_task(self.is_pressed())
	
	async def is_pressed(self):
		while True:
			if self.button.value() == 0:
				print('pressed')
				self.pressed = True
				await asyncio.sleep(0.3)
			await asyncio.sleep(0)

async def main():
	Pin(5,Pin.OUT).value(1)
	neo_time = Neo_time(Pin(6))
	button = Button(0)
	n = 1
	shapes = ('blocks','circles','random')
	show_task = asyncio.create_task(neo_time.show())
	await neo_time.set()
	while True:
		if button.pressed:
			neo_time.shape = shapes[n]
			print(neo_time.shape)
			n +=1
			if n == 3:
				n = 0
			button.pressed = False
		#reset correct time from network twice a day (hr min sec)
		if not(neo_time.rtc.datetime()[4] % 10) and neo_time.rtc.datetime()[5] == 5 and neo_time.rtc.datetime()[6] == 1:	 
			await neo_time.set()
		await asyncio.sleep(0.1)
#only activate weblink if no network parameters 
if not SSID:
	import weblink
else:
    asyncio.run(main())

