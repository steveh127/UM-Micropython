
from machine import Pin,I2S,WDT
import asyncio

from board import BUTTONS,i2c
from bling import Bling_Display

class Button():
	def __init__(self,pin):
		self._button=Pin(pin,Pin.IN,Pin.PULL_DOWN)
		self.pin=pin
		self.action=self.default_action
	
	def __call__(self):
		return self._button.value()
		
	async def default_action(self):
		print('Default Action: ' + str(self.pin))

class Console():
	
	def __init__(self):
		self.text=''
		self.buttons = []
		for button in BUTTONS:
			self.buttons.append(Button(button))
		self.display=Bling_Display()
		self.line=0
		self.set_vol=False
		self.up_vol=False
		self.down_vol=False
		self.mute=False	
		self.mute_vol=-3
		
	async def button_action(self,button):
		while True:
			if button() == 1:
				await button.action()
				await asyncio.sleep(0.3)
			await asyncio.sleep(0)
	
	async def show_text(self):
		while True:
			if self.text:
				txt=self.text.replace('_',' ')
				print(txt)
				await self.display.show(txt)
				self.text=''
			await asyncio.sleep(0)
	
	async def display_text(self,txt):
		self.text=txt
		while self.text:
			await asyncio.sleep(0)
						
	async def adjust_volume(self):
		wdt=WDT(timeout=5000)
		while True:
			wdt.feed()
			if self.set_vol:
				self.set_vol=False
				#save screen and button actions
				display_buffer=self.display.buffer[:]
				act0=self.buttons[0].action
				act1=self.buttons[1].action
				#volume actions
				self.buttons[0].action=self.up_volume
				self.buttons[1].action=self.down_volume
				self.line=3
				self.text='Up    Back  Down'
				while self.text:
					await asyncio.sleep(0)
				while True:
					wdt.feed()
					if self.up_vol:
						self.volume += 1
						if self.volume > 1:
							self.volume=1
						self.up_vol=False
						await asyncio.sleep(0.3)
					
					if self.down_vol:
						self.volume -= 1
						if self.volume < -12:
							self.volume = -12
						self.down_vol=False
						await asyncio.sleep(0.3)
								
					if self.set_vol:
						self.set_vol=False
						#restore screen and button actions
						self.display.buffer[:]=display_buffer
						self.display.show()
						self.buttons[0].action=act0
						self.buttons[1].action=act1
						break
						
					await asyncio.sleep(0)
			await asyncio.sleep(0)

	async def mute_now(self):
		if self.mute:
			self.mute=False
			self.volume=self.mute_vol
		else:
			self.mute=True
			self.mute_vol=self.volume
			self.volume=-16
		await asyncio.sleep(0.3)
		
	async def up_volume(self):
		print('up')
		self.up_vol=True
		await asyncio.sleep(0.3)	

	async def down_volume(self):
		print('down')
		self.down_vol=True
		await asyncio.sleep(0.3)
				
	async def console_tasks(self):
		self.display.setup_tasks()	
		asyncio.create_task(self.adjust_volume())
		for but in self.buttons:
			asyncio.create_task(self.button_action(but))
		
			
