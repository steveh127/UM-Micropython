import asyncio
from machine import Pin
from neopixel import NeoPixel
from time import sleep

class Colour():
	def __init__(self,pattern,brightness):
		self.pattern=pattern
		self.brightness=brightness
	
	def __call__(self,brightness=None):
		if brightness is None:
			brightness = self.brightness
		colour=[0,0,0]
		for i in range(3):
			if self.pattern[i]:
				colour[i]=int(brightness*self.pattern[i])
		return colour
                    
class Bling_Display(NeoPixel):
	
	
	def __init__(self):
		NeoPixel.__init__(self,Pin(18),320)
		self.power=Pin(6,Pin.OUT)
		self.power.on()
		self.brightness=5
		
		self.RED = Colour((1,0,0),self.brightness)
		self.GREEN = Colour((0,1,0),self.brightness)
		self.YELLOW = Colour((2,1,0),self.brightness)
		self.ORANGE = Colour((4,0.5,0),self.brightness)
		self.BLUE = Colour((0,0,1),self.brightness)
		self.PURPLE = Colour((3,0,1),self.brightness)
		self.WHITE = Colour((1,1,1),self.brightness)
		self.BLACK = Colour((0,0,0),self.brightness)
		
		self.lines=[0,40,80,120,160,200,240,280]
		
		self.screen=[]
		
		self.background=self.BLACK(1)
		
		self.text=''
		self.colour=self.GREEN()
		self.justify='C'
		self.scrolling=False	
		self.speed=0.2
		self.gap=1
		
		self.chars = {
	' ':('0','0','0','0','0','0'),
	'.':('0','0','0','0','0','1'),
	'!':('1','1','1','1','0','1'),
	',':('0','0','0','0','0','1','1'),
	':':('0','0','1','0','1','0'),
	';':('0','0','1','0','1','1'),
	'?':('110','001','001','010','000','010'),
	'"':('101','101','000','000','000','000'),
	
	'+':('000','000','010','111','010','000'),
	'-':('000','000','000','111','000','000'),
	'=':('000','000','111','000','111','000'),
	'\\':('100','100','010','010','001','001'),
	'/':('001','001','010','010','100','100'),
	'(':('01','10','10','10','10','01'),
	')':('10','01','01','01','01','10'),
	'[':('11','10','10','10','10','11'),
	']':('11','01','01','01','01','11'),
	'_':('0000','0000','0000','0000','0000','1111'),
	'<':('000','001','010','100','010','001'),
	'>':('000','100','010','001','010','100'),
	
	'0':('0110','1001','1001','1001','1001','0110'),
	'1':('01','11','01','01','01','01'),
	'2':('0110','1001','0001','0010','0100','1111'),
	'3':('1111','0001','0111','0001','0001','1110'),
	'4':('0010','0110','1010','1111','0010','0010'),
	'5':('1111','1000','1110','0001','0001','1110'),
	'6':('0010','0100','1000','1110','1001','0110'),
	'7':('1111','0001','0010','0100','0100','0100'),
	'8':('0110','1001','0110','1001','1001','0110'),
	'9':('0111','1001','1001','0111','0001','0001'),
	
	'A':('00100','01010','10001','11111','10001','10001'),
	'B':('1110','1001','1110','1001','1001','1110'),
	'C':('0111','1000','1000','1000','1000','0111'),
	'D':('1110','1001','1001','1001','1001','1110'),
	'E':('1111','1000','1110','1000','1000','1111'),
	'F':('1111','1000','1110','1000','1000','1000'),
	'G':('0111','1000','1000','1011','1001','0110'),		
	'H':('10001','10001','11111','10001','10001','10001'),
	'I':('111','010','010','010','010','111'),
	'J':('0111','0010','0010','0010','0010','1100'),
	'K':('1001','1010','1100','1100','1010','1001'),
	'L':('1000','1000','1000','1000','1000','1111'),
	'M':('10001','11011','10101','10001','10001','10001'),
	'N':('10001','11001','10101','10011','10001','10001'),
	'O':('01110','10001','10001','10001','10001','01110'),
	'P':('11110','10001','10001','11110','10000','10000'),
	'Q':('01110','10001','10001','10001','10101','01110','00001'),
	'R':('1110','1001','1001','1110','1010','1001'),
	'S':('0111','1000','1000','0110','0001','1110'),
	'T':('11111','00100','00100','00100','00100','00100'),
	'U':('1001','1001','1001','1001','1001','0110'),
	'V':('10001','10001','10001','10001','01010','00100'),
	'W':('10001','10001','10001','10101','10101','01010'),
	'X':('10001','01010','00100','00100','01010','10001'),
	'Y':('10001','10001','01010','00100','01000','01000'),
	'Z':('11111','00010','00100','01000','10000','11111'),
	
	'a':('0000','0110','0001','0111','1001','0111'),
	'b':('1000','1000','1110','1001','1001','1110'),
	'c':('000','011','100','100','100','011'),
	'd':('0001','0001','0111','1001','1001','0111'),
	'e':('0000','0110','1001','1111','1000','0111'),
	'f':('0011','0100','1110','0100','0100','0100'),
	'g':('0000','0111','1001','1001','0111','0001','0110'),
	'h':('1000','1000','1110','1001','1001','1001'),
	'i':('00','10','00','10','10','01'),
	'j':('001','000','001','001','001','001','110'),
	'k':('000','100','100','101','110','101'),
	'l':('110','010','010','010','010','111'),
	'm':('00000','11110','10101','10101','10101','10101'),
	'n':('0000','1110','1001','1001','1001','1001'),
	'o':('0000','0110','1001','1001','1001','0110'),
	'p':('0000','1110','1001','1001','1110','1000','1000'),	
	'q':('0000','0111','1001','1001','0111','0001','0001'),
	'r':('0000','0000','1011','1100','1000','1000'),
	's':('000','011','100','010','001','110'),
	't':('0000','0100','1111','0100','0100','0011'),		
	'u':('0000','1001','1001','1001','1001','0111'),
	'v':('000','000','101','101','101','010'),		
	'w':('00000','00000','10001','10001','10101','01010'),	
	'x':('00000','10001','01010','00100','01010','10001'),
	'y':('00000','10001','10001','01010','00100','01000','10000'),
	'z':('00000','11111','00010','00100','01000','11111'),
	
	'box':('111111','100001','100001','100001','100001','111111'),
	'Box':('111111','111111','111111','111111','111111','111111'),
	'TriR':('000001','000011','000111','001111','011111','111111'),
	'triR':('000001','000011','000101','001001','010001','111111'),
	'TriL':('100000','110000','111000','111100','111110','111111'),
	'triL':('100000','110000','101000','100100','100010','111111'),
	'arrowL':('000000','001000','011111','100001','011111','001000'),
	'ArrowL':('000000','001000','011111','111111','011111','001000'),
	'arrowR':('000000','000100','111110','100001','111110','000100'),
	'ArrowR':('000000','000100','111110','111111','111110','000100'),
	
	'Bar0':('000','000','000','000','000','000','000'),
	'Bar1':('000','000','000','000','000','000','111'),
	'Bar2':('000','000','000','000','000','111','111'),
	'Bar3':('000','000','000','000','111','111','111'),
	'Bar4':('000','000','000','111','111','111','111'),
	'Bar5':('000','000','111','111','111','111','111'),
	'Bar6':('000','111','111','111','111','111','111'),
	'Bar7':('111','111','111','111','111','111','111'),
	

	
	'RED':  ('#',self.RED),
	'GREEN':('#',self.GREEN),
	'BLUE': ('#',self.BLUE),
	'YELLOW': ('#',self.YELLOW),
	'ORANGE' : ('#',self.ORANGE),
	'PURPLE' : ('#',self.PURPLE),
	'WHITE' : ('#',self.WHITE),
	'BLACK' : ('#',self.BLACK),
	
	}
	
	
	def save_screen(self):
		self.screen=[]
		for r in range (8):
			row=[]
			for c in range (40):
			 row.append(self[self.lines[r]+c])
			self.screen.append(row)
	
	def restore_screen(self):
		for r in range (8):
			for c in range (40):
				self[self.lines[r]+c] = self.screen[r][c]
		self.write()
	
	def set_background(self,colour):
		self.save_screen()
		for r in range (8):
			for c in range (40):
			 if self[self.lines[r]+c] == tuple(self.background):
				self.screen[r][c] = colour
		self.background = colour
		self.restore_screen()
	
	async def scroll_screen(self):
		self.save_screen()
		stop=False
		while not stop and not self.scrolling:
			for row in range(8):
				if self.text:
					stop=True
				first=self.screen[row][0]
				self.screen[row]=self.screen[row][1:]
				self.screen[row].append(first)
			self.restore_screen()
			await asyncio.sleep(self.speed)
		await asyncio.sleep(0.1)
					
	def col(self,n,colour=None):
		if colour is None:
			colour=self.colour
		for line in self.lines:
			self[line+n] = colour
			self.write()

	def row(self,n,colour=None):
		if colour is None:
			colour=self.colour
		for i in range(40):
			self[self.lines[n]+i] = colour
		self.write()
		
	def show_char(self,char,col,colour=None):
		if colour is None:
			colour=self.colour
		if char not in self.chars.keys():
			char='.'
		character=self.chars[char]
		if character[0] == '#':
			self.colour = character[1](brightness=self.brightness)
			return 0
		width = len(character[0])
		line=1
		for row in character:
			p=0
			for c in row:
				if c == '1':
					self[self.lines[line]+col+p]=colour
				p += 1
			line += 1
		return width
		
	def length(self,text):
		length=0
		for c in text:
			if c not in self.chars.keys():
				c='.'
			if self.chars[c][0] != '#':
				length += len(self.chars[c][0]) + self.gap
		return length - self.gap
	
	async def show_text(self):
		while True:
			if self.text and not self.scrolling:
				self.fill(self.background)
				text=self.text
				lt = self.length(text)
				if lt > 38:
					self.scrolling=True
				else:
					self.scrolling=False
					if self.justify == 'C' or self.justify == 'R':
						if self.justify == 'C':
							column = (39 - lt)//2
						if self.justify == 'R':
							column = 39 - lt
					else:
						column=1
					for ch in text:
						width = self.show_char(ch,column,self.colour) + self.gap
						if width > self.gap:
							column += width							
					self.write()
					self.text=''
			await asyncio.sleep(0.2)
	

	
	def get_keys(self,text):
		key_list=[]
		shape_key=''
		for c in text:
			if c=='}':
				key_list.append(shape_key[1:])
				shape_key=''
				continue
			if shape_key:
				shape_key += c
				continue
			if c=='{':
				shape_key='1'
				continue
			key_list.append(c)
		return key_list

	async def show(self,text,colour=None,justify=None,brightness=None,scroll=False):
		if colour is not None:
			self.colour=colour
		if justify is not None:
			self.justify=justify
		if brightness is not None:
			self.brightness=brightness
		self.text=self.get_keys(text)
		while self.text :
			await asyncio.sleep(0)
		if scroll:
			await self.scroll_screen()
			
	def write_char(self,char,col):
		colour=self.colour
		if char not in self.chars.keys():
			char='.'
		character=self.chars[char]
		if character[0] == '#':
			self.colour = character[1](brightness=self.brightness)
			return 0
		width = len(character[0])
		line=1
		for row in character:
			p=0
			for c in row:
				if c == '1':
					self.text_buffer[line][col+p]=colour
				p += 1
			line += 1
		return width			
			
			
	async def scroll_text(self):
		while True:
			if self.scrolling:
				text=self.text
				self.text=''
				len_txt = self.length(text)
				self.text_buffer=[]
				for row in range(8):
					row=[]
					for col in range(len_txt+1):
						row.append(self.background)
					self.text_buffer.append(row)
				column=1
				for ch in text:
					width = self.write_char(ch,column) + self.gap
					if width > self.gap:
						column += width
				while self.scrolling:
					for line in self.lines:
						for c in range(40):
							self[line+c]=self.text_buffer[line//40][c]
					self.write()
					#do the scroll
					for row in range(8):
						first=self.text_buffer[row][:1]
						self.text_buffer[row]=self.text_buffer[row][1:]
						self.text_buffer[row].append(first[0])
					await asyncio.sleep(self.speed)
					if self.text:
						self.scrolling=False
			await asyncio.sleep(0)
			
	async def clear(self):
		self.text=' '
		while self.text:
			await asyncio.sleep(0)
		self.fill((0,0,0))
		self.write()			


	async def bar_chart(self,*args,high=7,colour='{BLUE}',pre='',post=''):
		bars=('{Bar0}','{Bar1}','{Bar2}','{Bar3}','{Bar4}','{Bar5}','{Bar6}','{Bar7}')
		chart=pre
		step = high/7
		for value in args:
			h=int(value[0] // step)
			if h > 7:
				h=7
				chart += '{RED}'
			else:
				if len(value) > 1:
					chart += value[1]
				else:
					chart += colour
			chart += bars[h]
		chart += post
		await self.show(chart)

class Bling_Buttons():
	def __init__(self,actions):
		buttons=[11,10,33,34]
		self.buttons=[[],[],[],[]]
		for i,button in enumerate(buttons):
			self.buttons[i]=(Pin(button,Pin.IN),actions[i])
		
	async def check(self):
		while True:
			for button in self.buttons:
				if button[0].value():
					action=button[1]
					await action()
					await asyncio.sleep(0.4)
			await asyncio.sleep(0)

			
