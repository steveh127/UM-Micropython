import asyncio
from machine import Pin,PWM,I2C
from neopixel import NeoPixel
import ntptime
from time import localtime

from led_multi_as import LED_Multi_AS

from config import DS,HR24,OFFSET

'''
classes to manage Unexpected Makers WOPR display which has 12 15 bit LED displays controlled by 3 HT16K33 chips.
also controls RGB neopixel array, buttons and buzzer.

asyncio version

'''

class RGB_LED():
	
	OFF,RED,GREEN,BLUE,YELLOW,WHITE = ((0,0,0),(20,0,0),(0,20,0),(0,0,20),(20,20,0),(20,20,20))
	
	def __init__(self,neopixel,number):
		self.np=neopixel
		self.number=number
		self.period=1
		self.toggle=False
		self.is_on=False
		self.colour=self.WHITE
		self.to_flash=False
	
	def set(self):
		self.np[self.number-1]=self.colour
		self.np.write()
		self.is_on=True
					
	def clear(self):
		self.np[self.number-1]=self.OFF
		self.np.write()
		self.is_on=False
	
	def on(self):
		if not self.is_on:
			self.toggle=True
	
	def off(self):
		if self.is_on:
			self.toggle=True
			
	
	async def flash(self,period=None):
		if period is not None:
			self.period=period
		if not self.is_on:
			self.set()
		else:
			self.clear()
		await asyncio.sleep(self.period)
		if not self.is_on:
			self.set()
		else:
			self.clear()
		self.to_flash=False

class WOPR():
	
	OFF,RED,GREEN,BLUE,YELLOW,WHITE = ((0,0,0),(20,0,0),(0,20,0),(0,0,20),(20,20,0),(20,20,20))
	
	#default pins for UM TinyPICO S2 as installed on WOPR - I2C required is I2C(0) on TinyPICO
	def __init__(self, i2c,*,rgb=27,buzz=25,b1=15,b2=14,b3=32,b4=33):
		#main LED display
		self.display=LED_Multi_AS(I2C(0),(112,114,116))
		self.display.set_brightness(5)
		self.display.flush()
		self.display.update()
		#rgb LEDs
		self.rgb=NeoPixel(Pin(rgb),5)
		self.rgb_led1=RGB_LED(self.rgb,1)
		self.rgb_led2=RGB_LED(self.rgb,2)
		self.rgb_led3=RGB_LED(self.rgb,3)
		self.rgb_led4=RGB_LED(self.rgb,4)
		self.rgb_led5=RGB_LED(self.rgb,5)
		self.rgb_led1.colour,self.rgb_led2.colour,self.rgb_led3.colour,self.rgb_led4.colour,self.rgb_led5.colour=(self.RED,self.GREEN,self.BLUE,self.YELLOW,self.WHITE)
		self.rgb_leds=[self.rgb_led1,self.rgb_led2,self.rgb_led3,self.rgb_led4,self.rgb_led5]
		#for led in self.rgb_leds:
			#led.on()
		#buzzer
		self.buzzer=PWM(Pin(buzz))
		self.buzzer.deinit()
		self.beep_length=0.1
		self.beep_freq=1000
		self.to_beep=True
		#buttons
		self.buttons=(Pin(b1,Pin.IN,Pin.PULL_DOWN),
					  Pin(b2,Pin.IN,Pin.PULL_DOWN),
					  Pin(b3,Pin.IN,Pin.PULL_DOWN),
					  Pin(b4,Pin.IN,Pin.PULL_DOWN)
		)
		#Pin(2,Pin.OUT).value(1)
		self.action=[None,None,None,None]
		#clock
		self.clock_running=False
		self.daylight_saving=DS
		self.twenty4=HR24
		self.offset=OFFSET
		#IP address
		self.IP='0.0.0.0'
		self.show_IP=False
	
	#Main LED sequence Control	
	def clear_leds(self):
		self.display.clear()
	
	def update(self):
		self.display.update()
			
	def set_brightness(self,brightness):
		if brightness < 0:
			brightness = 0
		if brightness > 15:
			brightness = 15
		self.display.set_brightness(brightness)
	
	def show_number(self,number,*,justify='L'):
		self.display.justify=justify
		self.display.value=number
		
	
	def show_string(self,string,*,justify='C',loop=False):
		dc=0
		for c in string:
			if c == '.':
				dc += 1
		if (len(string)-dc) < 13:
			self.display.clear()
			self.display.justify=justify
			self.display.value=string
		else:
			self.scroll_string(string,speed=0.3,loop=loop)

	def scroll_string(self,string,*,speed=1,loop=False):
		self.display.scrolling=True
		self.display.scroll_string=string
		self.display.scroll_speed=speed
		self.display.scroll_loop=loop
	
	def save_config(self):
		with open('config.py','wb') as cf:
			if self.daylight_saving:
				cf.write('DS=True\n')
			else:
				cf.write('DS=False\n')
			if self.twenty4:	
				cf.write('HR24=True\n')
			else:
				cf.write('HR24=False\n')
			cf.write('OFFSET=' + str(self.offset) + '\n')
			
	#button actions
	def set_action(self,button_number,action):
		self.action[button_number]=action
	
	def set_actions(self,actions):
		for i in range(4):
			self.set_action(i,actions[i])
			
	#coroutines
	async def clear(self):
		self.clock_running=False
		self.string=' '
		for led in self.rgb_leds:
			led.off()
		await asyncio.sleep(1)
		self.string=''
	
	async def beep(self):
		self.buzzer.init(self.beep_freq)
		await asyncio.sleep(self.beep_length) 
		self.buzzer.deinit()
		self.to_beep=False		
			
	#coroutines run as asyncio tasks 	
	async def check_pressed(self,button_number):
		while True:
			if self.buttons[button_number].value() == 1:
				await self.action[button_number]()
				await asyncio.sleep(0.1)
			await asyncio.sleep(0)
	
	async def check_rgb_leds(self):
		while True:
			for rgb_led in self.rgb_leds:
				if rgb_led.to_flash:
					await rgb_led.flash()
				if rgb_led.toggle:
					if rgb_led.is_on:
						rgb_led.clear()
					else:
						rgb_led.set()
					rgb_led.toggle=False
			await asyncio.sleep(0.1)
	
	async def check_beep(self):
		while True:
			if self.to_beep:
				await self.beep()
			await asyncio.sleep(0.1)
			
	async def check_IP(self):
		while True:
			if self.show_IP:
				self.display.flush()
				self.display.justify='C'
				self.display.value=self.IP
				self.show_IP=False
			await asyncio.sleep(0.1)
		
	#clock functions

	#must only be called after network connection established
	def set_time(self):
		NTP_SERVER = '0.ch.pool.ntp.org'
		ntptime.host = NTP_SERVER
		while True:
			try:
				ntptime.settime()
				print('Time Set')
			except OSError as e:
				print(e)
			else:
				break
				
	async def clock(self):
		count=0
		while True:		
			if self.clock_running:
				yr,mnth,day,hr,mn,sec,_,_ = localtime()
				hr += self.offset
				if hr > 23:
					hr -= 24
				if hr < 0:
					hr += 24
				if self.daylight_saving:
						hr += 1
						if hr == 24:
							hr = 0
				if not self.twenty4:
					if hr > 12:
						hr -= 12
					if hr==0:
						hr=12
				time = [str(hr),str(mn),str(sec)]
				for i in range(3):
					if len(time[i])==1:
						time[i] = '0' + time[i]
				if not self.twenty4 and hr < 10:
					time[0] = ' ' + time[0][1]
				self.display.value = '  ' + time[0] + '-' + time[1] + '-' + time[2]
			#reset time every 12 hours
			count += 1
			if count == 60 * 60 * 12:
				count=0
				self.set_time()
			await asyncio.sleep(1)
		
	def start_clock(self):
		self.clock_running=True
	
	def stop_clock(self):
		self.clock_running=False
		
	def toggle_clock(self):
		self.clock_running = not self.clock_running
		if not self.clock_running:
			self.display.clear()
		await asyncio.sleep(0.5)
	
	async def display_IP(self):
		self.clock_running = False
		self.show_IP=True
		await asyncio.sleep(0.5)
		
	async def toggle_ds(self):
		if self.daylight_saving:
			self.daylight_saving=False
		else:
			self.daylight_saving=True
		self.save_config()
	
	async def toggle_24(self):
		if self.twenty4:
			self.twenty4=False
		else:
			self.twenty4=True
		self.save_config()
			
	#sets up check tasks for async operation
	async def check(self):
		await self.display.setup_tasks()
		asyncio.create_task(self.check_rgb_leds())
		asyncio.create_task(self.check_beep())
		asyncio.create_task(self.clock())
		asyncio.create_task(self.check_IP())
		for i in range(4):
			asyncio.create_task(self.check_pressed(i))
			
from board import RGB,BUZZ,B1,B2,B3,B4			
				
def active_WOPR():
	wopr = WOPR(I2C(0),rgb=RGB,buzz=BUZZ,b1=B1,b2=B2,b3=B3,b4=B4)
	#tie actions to buttons
	wopr.set_actions((wopr.display_IP,wopr.toggle_clock,wopr.toggle_ds,wopr.toggle_24))
	def get():
		nonlocal wopr
		return wopr	
	return get
	
get_WOPR=active_WOPR()
