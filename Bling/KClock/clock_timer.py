'''
Driver program for a kitchen clock / timer.

Hardware required:

Network capable MCU running micropython. .
Display with a driver having a show_time funcion that takes a time tuple (min,secs or hour/min)
and displays it, with no arguments show_time blanks the display.
2 buttons, set and start, active low.
Single RGB neopixel.
Buzzer.

Network is only used to set time. 

Functionality.

Starts in clock mode. Clock display can be toggled with 'Start' button.

Pressing set enters timer mode showing 00:00

Set button is used to set minutes. Start initiates countdown.
Beeps and flashes at end. Set clears alarm and returns to clock. 
If Set is pressed during count return to clock,

With display zeroed Start initiates stopwatch mode. This counts up until Set is
pressed which holds display. Pressing Set again returns to clock.

Pressing Start when timing pauses timer, can restart timing with Start or return to Clock
with Set. 

Tested with Seed Studio XIAO ESP32 C3. 
Display used was a 4 character 7 segment LED driven via an TM1637

'''

import uasyncio as asyncio
from machine import Pin, RTC

from net_tools import Network_Tools
from bling import Bling_Display

class Alarm():
	#datetime=(yr,month,day,hr,min) with yr,month,day optional.
	def __init__(self,datetime,*,action=None,active=True,repeat=False):
		if len(datetime)==5:
			self.date=datetime[0:3]
			self.time=datetime[3:5]
		else:
			self.date=None
			self.time=datetime
		self.action=action
		self.active=active
		self.repeat=repeat
	
	def check(self,datetime):
		if self.active:
			date=datetime[0:3]
			time=datetime[3:5]
			if date==self.date and time==self.time:
				self.active=False
				self.action()
			if time==self.time and self.date is None:
				if not self.repeat:
					self.active=False
				self.action()

class Clock(Network_Tools):
	
	def __init__(self,show_time,*,show=True):
		self._show_time = show_time
		self.blank()
		self.set_time()
		self.disconnect()
		self.rtc=RTC()
		self._get_time()
		self.blank()
		self.show=show
		self.alarms=[]
				
	def _get_time(self):
		self.yr,self.mn,self.dy,self.dow,self.hr,self.min,self.sec,_ = self.rtc.datetime()
		self.datetime=(self.yr,self.mn,self.dy,self.hr,self.min)	
	
	async def show_time(self):
		await self._show_time((self.hr,self.min))
		
	async def blank(self):
		await self._show_time()
	
	def set_alarm(self,datetime,action):
		self.alarms.append(Alarm(datetime,action=action))
	
	async def check_alarms(self):
		while True:
			if self.sec == 0:
				for alarm in self.alarms:
					if alarm.active:
						alarm.check(self.datetime)
			await asyncio.sleep(1)
						
	async def run(self):
		self._get_time()
		on = False
		while True:
			self._get_time()
			if self.show:
				if self.sec == 0 or not on:
					on=True
					await self.show_time()
			else:
				on=False
				await self._show_time()
			await asyncio.sleep(1)
RED='RED'
GREEN='GREEN'
BLUE='BLUE'

class ClockTimer():
	#show_time is a function that takes a time tuple (min,secs) and updates a display, 
	#rgb is GPIO pin for a single rgb neopixel, a 'UniPixel' 
	
	def __init__(self,mins=0,secs=0):
		self.display=Bling_Display()
		self.display.setup_tasks()
		self.display.text='Setting Time'
		self.show_time = self.display.show_time
		#self.rgb = UniPixel(rgb)
		#self.buzz = buzzer
		self.__mins = mins
		self.__secs = secs
		self.mins = mins
		self.secs = secs
		self.clock=Clock(self.show_time)
		self.state= 'clock_on'
		
	def rgb(self,colour):
		print(colour)
	
	@property
	def state(self):
		return self.__state
	
	@state.setter
	def state(self,state):
		self.__state = state
		if state == 'clock_on':
			self.clock.show=True
		if state == 'clock_off':
			self.clock.show=False
		if state == 'ready':
			self.rgb(BLUE)
			self.mins,self.secs = 0,0
		if self.state == 'run_paused' or self.state == 'timer_paused':
			self.rgb(BLUE)
		if state == 'running' or state == 'timing':
			self.rgb(GREEN)
		if state == 'finished' or state == 'timed':
			self.rgb(RED)	
	
	@property
	def mins(self):
		return self.__mins
	
	@mins.setter
	def mins(self,m):
		self.__mins = m
		#await self.show_time((self.__mins,self.__secs))	
	
	@property
	def secs(self):
		return self.__secs
	
	@secs.setter
	def secs(self,s):
		self.__secs = s
		#await self.show_time((self.__mins,self.__secs))
	
	def _toggle(self,colour):
		if self.secs % 2:
			self.rgb(colour)
		else:
			self.rgb('Clear')
			
	#extra state checks are there to handle change of state while in 
	#timing loop.		
	async def count_down(self):
		while True:
			while (self.mins + self.secs) > 0 and self.state == 'running':
				await asyncio.sleep(1)
				if self.state == 'running':
					if self.secs == 0:
						self.mins -=1
						self.secs = 59
					else:
						self.secs -=1
					self._toggle(GREEN)
			if self.state == 'running':		
				self.state='finished'
			await asyncio.sleep(0)
					
	async def count_up(self):
		while True:
			while self.state == 'timing':
				await asyncio.sleep(1)
				s = self.secs
				m = self.mins
				if self.state == 'timing':
					s += 1
					if s == 60:
						s = 0
						m += 1
					self.secs = s
					self.mins = m
					self._toggle(GREEN)
			await asyncio.sleep(0)
	
	#flashes an LED and beeps while 'finished' 			
	async def finish(self):
		while True:
			if self.state == 'finished':
				self.buzz.on()
				await asyncio.sleep(0.2)
				self.buzz.off()
				if self.state == 'finished':
					self.rgb(RED)
				await asyncio.sleep(0.5)
				if self.state == 'finished':
					self.rgb('Clear')
			await asyncio.sleep(0)
	
	async def state_machine(self,b_set,b_start):
		while True:
			if b_set.value():
				if self.state == 'ready':
					self.mins +=1
					await asyncio.sleep(.3)
				if self.state=='clock_on' or self.state=='clock_off' :
					self.clock.show=False
					await  asyncio.sleep(1)
					self.state='ready'
					#self.mins,self.secs = 0,0
				if self.state == 'timing' or self.state == 'timed':
					if self.state == 'timing':
						self.state = 'timed'
					else:	
						self.state = 'clock_on'
					await asyncio.sleep(.3)
				if self.state == 'running' or self.state == 'run_paused' or self.state == 'timer_paused': 
					await asyncio.sleep(.3)		
					self.state = 'clock_on'
				if self.state == 'finished':
					self.buzz.off()
					await asyncio.sleep(.3)		
					self.state = 'clock_on'

			if b_start.value():
				if self.state=='clock_on':
					self.state = 'clock_off'
					await asyncio.sleep(.3)
				else:
					if self.state=='clock_off':
						self.state = 'clock_on'
						await asyncio.sleep(.3)
				if self.state == 'running' or self.state == 'run_paused':
					if self.state == 'running':
						self.state = 'run_paused'
					else:
						self.state = 'running'
					await asyncio.sleep(.3)
				if self.state == 'timing' or self.state == 'timer_paused':
					if self.state == 'timing':
						self.state = 'timer_paused'
					else:
						self.state = 'timing'
					await asyncio.sleep(.3)				
				if self.state == 'ready':
					if self.mins:
						self.state = 'running'
					else:
						self.state = 'timing'
					await asyncio.sleep(.3)
			await asyncio.sleep(0)
			
	async def new_time(self):
		m=self.mins
		s=self.secs
		while True:
			if m != self.mins or s != self.secs:
				m=self.mins
				s=self.secs
				await self.show_time((m,s))
			await asyncio.sleep(0.2)
			
	async def setup_tasks(self,b_set,b_start):
		asyncio.create_task(self.new_time())
		asyncio.create_task(self.count_down())
		asyncio.create_task(self.count_up())
		asyncio.create_task(self.finish())
		asyncio.create_task(self.state_machine(b_set,b_start))
		asyncio.create_task(self.clock.run())
		
ct=ClockTimer()

b_set   = Pin(11,Pin.IN)
b_start = Pin(33,Pin.IN)

async def main():
	
	await ct.setup_tasks(b_set,b_start)
	while True:
		await asyncio.sleep(10)

asyncio.run(main())
