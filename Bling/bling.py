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
                    
class Bling(NeoPixel):
	chars={
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
	'1':('010','110','010','010','010','010'),
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
	'J':('011','001','001','001','001','110'),
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
	'z':('00000','11111','00010','00100','01000','11111')	
	}
	
	
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
		
		self.background=self.BLACK(0)
		
		self.text=''
		self.colour=self.GREEN()
		self.justify='C'
		self.scrolling=False
		self.scroll_text=''		
		self.speed=0.2


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
		character=self.chars[char]
		width = len(character[0])
		line=1
		for row in character:
			p=0
			for c in row:
				if c == '1':
					self[self.lines[line]+col+p]=colour
				p += 1
			line += 1
		self.write()
		return width
	
	async def show_text(self):
		while True:
			if self.text and not self.scrolling:
				self.fill(self.background)
				text=self.text
				lt = 0
				for c in text:
					lt += len(self.chars[c][0]) + 1
				lt -= 1
				if lt > 38:
					self.scroll_text=text
					self.text=''
					self.scrolling=True
				else:
					if self.justify == 'C' or justify == 'R':
						if self.justify == 'C':
							column = (39 - lt)//2
						if self.justify == 'R':
							column = 39 - lt
					else:
						column=1
					colour=self.colour
					for ch in text:
						column += self.show_char(ch,column,colour) + 1
					self.text=''
			await asyncio.sleep(0)
	
	async def scroll(self):
		while True:
			if self.scroll_text:
				text=self.scroll_text
				self.scroll_text=''
				self.scrolling=True
				rows=['','','','','','','']
				for c in text:
					char = self.chars[c]
					for i in range(6):
						rows[i] += char[i] + '0'
					if len(char)==7:
						rows[6] += char[6] + '0'
					else:
						rows[6] += len(char[0])*'0' + '0'
				colour=self.colour
				speed=self.speed
				while self.scrolling:	
					for start in range(-40,len(rows[0])):
						self.fill(self.background)					
						for i in range(7):
							for col in range (0,38):
								if (col+start) < len(rows[0]) and (col+start) > -1:
									if rows[i][col + start] == '1':
										self[self.lines[i+1] + col + 1]=self.colour
						self.write()
						await asyncio.sleep(self.speed)
					if self.text or self.scroll_text:
						self.scrolling=False
					await asyncio.sleep(0.2)
			await asyncio.sleep(0)
		

async def main():
	d=Bling()
	d.background=(d.GREEN(1))
	d.fill(d.background)
	asyncio.create_task(d.show_text())
	asyncio.create_task(d.scroll())
	d.colour=d.RED()
	d.text='123456'
	await asyncio.sleep(5)
	d.text='ABCDEFGHIJK'
	while True:
		await asyncio.sleep(5)
		d.text='ZZZZ'
asyncio.run(main())
	
