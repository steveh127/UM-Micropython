from ht16k33 import HT16K33
import asyncio

'''
class to manage multiple 4 character 15 bit LED displays controlled by multiple HT16K33 chips.
Character mapping is as for Adafruit Feather displays.

async version.

Mapping of LEDs to Positions. First Byte 1,2,4,8,16,32 round edge clockwise starting at top.
Second Byte is Inner Diagonals, Middle Line and Decimal Point(64) 

      First Byte         Second Byte

	      1              1    2   4
	32		   2          .   .   .
	                        . . .
	   64  128                x
                            . . .
    16         4          .   .   .
          8              8   16   32  .64
          

'show' takes a number or a string .

'show' can be L,R or C justified. L is default.

All the above methods are just updating the display buffer, to display them use the 'update' method.

There is also a 'scroll' method which requires a string. Scrolling is L to R.

'show_time' is provided for compatibility with KCLOCK. time is supplied as a tuple and called without
argument clears display. Default justification is C

'''

class LED_Multi_AS():
	
	CHARSET={
		' ':(0,0),
		'A':(247,0),'B':(252,0),'C':(57,0),'D':(222,0),'E':(249,0),'F':(241,0),'G':(189,0),'H':(246,0),'I':(9,18),
		'J':(30,0),'K':(112,36),'L':(56,0),'M':(54,5),'N':(54,33),'O':(63,0),'P':(243,0),'Q':(63,32),'R':(243,32),
		'S':(237,0),'T':(1,18),'U':(62,0),'V':(48,12), 'W':(54,40),'X':(0,45),'Y':(0,21),'Z':(9,12),
		'0':(63,0),'1':(6,0),'2':(219,0),'3':(207,0),'4':(230,0),'5':(237,0),'6':(253,0),'7':(7,0),'8':(255,0),'9':(231,0),
		'.':(0,64),'?':(131,16),'-':(128,0),'+':(192,18),'=':(200,0),'<':(0,36),'>':(0,9),'/':(0,12),'\\':(0,33),'"':(0,2)
		}
	
	#LED sets must have different I2C addresses arranged lowest to highest address, left to right.
	#Alternatively addresses can be supplied as tuple in correct order.
	def __init__(self, i2c,I2C_addresses=None):
		self.led_sets=[]
		#mapping of digits to buffer addresses
		self.led_digits=[16,18,20,22]
		if I2C_addresses:
			for address in I2C_addresses:
				self.led_sets.append(HT16K33(i2c,address))
		else:
			LEDs=i2c.scan()
			for LED in LEDs:
				self.led_sets.append(HT16K33(i2c,LED))
		self.clear()
		#values for asyncio use
		self.time=None
		
		self.value=None
		self.justify='L'
		
		self.scrolling=False
		self.scroll_string=''
		self.scroll_speed=1
		self.scroll_loop=False
		self._scroll_done=True
		
		self.source=None
		self.streaming=False
		
	def update(self):
		for led_set in self.led_sets:
			led_set.update()	
	
	#clears buffer and display
	def clear(self):
		for led_set in self.led_sets:
			led_set.clear()
			led_set.update()
	
	#just clears buffer
	def flush(self):
		for led_set in self.led_sets:
			led_set.clear()
			
	def set_brightness(self,brightness):
		if brightness < 0:
			brightness = 0
		if brightness > 15:
			brightness = 15
		for ls in self.led_sets:
			ls.set_brightness(brightness)
			
	def _add_point(self,digit):
		digit -= 1
		ls = digit // 4
		led_set = self.led_sets[ls]
		d  = digit - ls * 4
		if led_set.buffer[self.led_digits[d]] + led_set.buffer[self.led_digits[d]+1]:
			led_set.buffer[self.led_digits[d]+1] += 64
					
	def set_char(self,digit,char):
		ls = digit // 4
		led_set = self.led_sets[ls]
		d  = digit - ls * 4
		led_set.buffer[self.led_digits[d]],led_set.buffer[self.led_digits[d]+1] = self.CHARSET[char]			
	
	
	def _show(self,value,justify='L'):
		if str(type(value)) == "<class 'float'>" or str(type(value)) == "<class 'int'>":
					value = str(value)
		string=value.upper()
		dc=0
		for c in string:
			if c=='.':
				dc += 1
		if len(string) > 12 + dc:
			string=string[0:12 + dc]
		if justify=='L':
			d = 0
		if justify=='R':
			d = 12 - len(string)
			d += dc
		if justify=='C':
			l=len(string)
			l -= dc
			d = (12 - l)//2
		for char in string:
			if char == '.':
				self._add_point(d)
				d-=1
			else:
				self.set_char(d,char)
			d+=1
	
	#supplied value can be string or number					
	async def show(self):
		while True:
			if self.value:
				self.scrolling=False
				self.streaming=False
				while not self._scroll_done:
					await asyncio.sleep(0)
				self._show(self.value,self.justify)
				self.update()
				self.value=None
			await asyncio.sleep(0.1)
	
	async def stream(self):
		while True:
			if self.streaming:
				if self.scrolling:
					self.scrolling=False
					while not self._scroll_done:
						await asyncio.sleep(0)
				string=''
				self._scroll_done=False
				while self.streaming:
					c=self.source()
					string = string[1:] + c
					self._show(string)
					self.update()
					await asyncio.sleep(self.scroll_speed)
			if not self._scroll_done:
				self.flush()
				self._scroll_done=True
			await asyncio.sleep(0.2)
						
	#any length string can be supplied - includes 'update'
	async def scroll(self):
		while True:
			if self.scrolling:
				if self.streaming:
					self.streaming=False
					while not self._scroll_done:
						await asyncio.sleep(0)
				self._scroll_done=False
				start_str = self.scroll_string
				#all . replaced with - to fix index error
				start_str = start_str.replace('.','-')
				self.clear()
				while self.scrolling:
					string = '            ' + start_str
					for _ in range(len(string) + 3):
						if not self.scrolling:
							break
						self.flush()	
						self._show(string)
						self.update()
						await asyncio.sleep(self.scroll_speed)
						string = string[1:] + ' '
					if not self.scroll_loop:
						self.scrolling=False
						break
			if not self._scroll_done:
				self._scroll_done=True		
			await asyncio.sleep(0.2)
	
	#time is a tuple (h,m),(h,m,s) or (m,s) 
	async def show_time(self,*,justify='C'):
		while True:
			if self.time:
				self.scrolling=False
				self.streaming=False
				while not self._scroll_done:
					await asyncio.sleep(0)
				time=list(self.time)
				ts=''
				for t in time:
					t=str(t)
					if len(t)==1:
						t='0'+t
					ts += t + '-'
				ts=ts[:-1]
				self.flush()
				self._show(ts,justify=justify)
				self.update()
				self.time=None
			await asyncio.sleep(0.2)
			
		
	async def setup_tasks(self):
		asyncio.create_task(self.show_time())
		asyncio.create_task(self.show())
		asyncio.create_task(self.scroll())
		asyncio.create_task(self.stream())
