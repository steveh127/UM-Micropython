import asyncio
from machine import Pin, RTC
import network
import ntptime
import sys

from squixl_text import *

from config import SSID,PSWD,H12,OFFSET

class SQ_Time():
	def __init__(self,x,y,colour,*,font):
		self.x = x
		self.y = y
		self.colour = colour
		self.font = font 
		self.UTC_offset = OFFSET
		self.ds  = False
		self.H12 = H12
		self.scr = get_screen()
		self.font = font
		self.rtc = RTC()
		self.rtc.datetime((2022,1,1,1,19,59,0,0)) #(year,month,day,day of week,hour,minute,second,subsecond)
		
		asyncio.create_task(self.show_time())		
		
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
		while True:
			try:
				net.connect(SSID,PSWD)
			except OSError as e:
				await asyncio.sleep(0.1)
			if net.isconnected():
				print('Connected') 
				break
		#set time from network
		NTP_SERVER = '0.ch.pool.ntp.org'
		ntptime.host = NTP_SERVER
		i = 0
		while i < 100:
			i += 1
			try:
				ntptime.settime()
				print('Time Set')
				break
			except OSError as e:
				print(e)
				await asyncio.sleep(1)
			else:
				break
		#disconnect from network
		net.disconnect()
		self._set_ds()
		
	def on_off(self):
		self.on = not self.on	
			
	async def show(self):
		print(self.rtc.datetime())
		while True:
			print(self.get_time())
			await asyncio.sleep(1)
	
	#used by text display to generate time as a string		
	def get_time(self):
		(yr,mnth,day,dow,hr,mnt,sec,_) = self.rtc.datetime()
		if self.UTC_offset:
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
		str_min = str(mnt)
		if len(str_min) == 1:
			str_min = '0' + str_min
		str_hr = str(hr)
		if len(str_hr) == 1:
			str_hr = '0' + str_hr
		str_sec = str(sec)
		if len(str_sec) == 1:
			str_sec = '0' + str_sec
		return str_hr,str_min,str_sec
				
	async def show_time(self):
		await self.set()
		while True:
			hr,mn,sec = self.get_time()
			time = hr + ' '+ mn + ' ' + sec
			self.scr.write_over(time,self.x,self.y, self.colour,font=self.font)
			await asyncio.sleep(1)


