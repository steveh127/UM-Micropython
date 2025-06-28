from machine import Pin
from neopixel import NeoPixel
from time import sleep

import asyncio

#support class to define RGB colours with controllable brightness.
class Colour():
	
	order=(0,1,2) #RGB
	
	def __init__(self,pattern,brightness):
		self.pattern=pattern
		self.brightness=brightness
	
	def __call__(self,brightness=None):
		if brightness is None:
			brightness = self.brightness
		colour =[0,0,0]
		order = self.order 
		oi = 0
		for i in range(3):
			if self.pattern[i]:
				colour[order[oi]]=int(brightness*self.pattern[i])
			oi += 1
		return colour

	
class NeoText(NeoPixel):
	
	def __init__(self,pin,*,neo_size,screen_map=None,columns,rows,charset=None):
		NeoPixel.__init__(self,pin,neo_size)
		
		self.cols = columns
		self.rows = rows
		
		self.brightness=2
		
		self.RED = Colour((1,0,0),self.brightness)
		self.GREEN = Colour((0,1,0),self.brightness)
		self.YELLOW = Colour((2,1,0),self.brightness)
		self.ORANGE = Colour((4,0.5,0),self.brightness)
		self.BLUE = Colour((0,0,1),self.brightness)
		self.PURPLE = Colour((3,0,1),self.brightness)
		self.WHITE = Colour((1,1,1),self.brightness)
		self.BLACK = Colour((0,0,0),self.brightness)
		
		self.lines=[]
		for i in range(self.rows):
			self.lines.append(self.cols * i)
		
		self.text = ''
		self.just = 'C'
		self.colour=self.GREEN()	
		self.background = self.BLACK()
		self.smap = screen_map
		self.start_line = 0
		asyncio.create_task(self.show_text())
		
		if charset is None:					
			self.chars = {
' ':('0000','0000','0000','0000','0000','0000'),
'.':('00','00','00','00','00','10'),
'!':('10','10','10','10','00','10'),
',':('00','00','00','00','10','10'),
':':('00','0','1','0','1','0'),
';':('00','0','1','0','1','1'),
'?':('110','001','001','010','000','010'),
'"':('1010','101','000','000','000','000'),

'+':('0000','000','010','111','010','000'),
'-':('0000','000','000','111','000','000'),
'=':('0000','000','111','000','111','000'),
'\\':('1000','100','010','010','001','001'),
'/':('0010','001','010','010','100','100'),
'(':('010','10','10','10','10','01'),
')':('100','01','01','01','01','10'),
'[':('110','10','10','10','10','11'),
']':('110','01','01','01','01','11'),
'_':('0000','0000','0000','0000','0000','1111'),
'<':('0000','001','010','100','010','001'),
'>':('0000','100','010','001','010','100'),

'0':('01100','10010','10010','10010','10010','01100'),
'1':('010','110','010','010','010','010'),
'2':('01100','1001','0001','0010','0100','1111'),
'3':('1110','001','111','001','001','110'),
'4':('00100','0110','1010','1111','0010','0010'),
'5':('11110','1000','1110','0001','0001','1110'),
'6':('00100','0100','1000','1110','1001','0110'),
'7':('11110','0001','0010','0100','0100','0100'),
'8':('01100','1001','0110','1001','1001','0110'),
'9':('01100','1001','1001','0111','0001','0010'),

'A':('001000','01010','10001','11111','10001','10001'),
'B':('11100','1001','1110','1001','1001','1110'),
'C':('01110','1000','1000','1000','1000','0111'),
'D':('11100','1001','1001','1001','1001','1110'),
'E':('11110','1000','1110','1000','1000','1111'),
'F':('11110','1000','1110','1000','1000','1000'),
'G':('01110','1000','1000','1011','1001','0110'),		
'H':('10010','1001','1111','1001','1001','1001'),
'I':('1110','010','010','010','010','111'),
'J':('01110','0010','0010','0010','0010','1100'),
'K':('10010','1010','1100','1100','1010','1001'),
'L':('10000','1000','1000','1000','1000','1111'),
'M':('100010','11011','10101','10001','10001','10001'),
'N':('100010','11001','10101','10011','10001','10001'),
'O':('01100','1001','1001','1001','1001','0110'),
'P':('11100','1001','1001','1110','1000','1000'),
'Q':('011100','10010','10010','01110','00011','00010'),
'R':('11100','1001','1001','1110','1010','1001'),
'S':('01110','1000','1000','0110','0001','1110'),
'T':('111110','00100','00100','00100','00100','00100'),
'U':('10010','1001','1001','1001','1001','0110'),
'V':('100010','10001','10001','10001','01010','00100'),
'W':('100010','10001','10001','10101','10101','01010'),
'X':('000000','10001','01010','00100','01010','10001'),
'Y':('100010','10001','01010','00100','00100','00100'),
'Z':('00000','1111','0010','0100','1000','1111'),

'x':('0000','0000','1010','0100','1010','0000'),
'o':('0000','0100','1010','1010','0100','0000'),

'b':('11111','10001','10001','10001','10001','11111'),
'c':('11111','11111','11111','11111','11111','11111'),

'l':('0000000','0010000','011111','100001','011111','001000'),
'r':('0000000','0001000','111110','100001','111110','000100'),
'u':('0010000','01010','11011','01010','01010','01110'),
'd':('0111000','01010','01010','11011','01010','00100'),
's':('0001000','001010','110001','100010','100100','111100'),
'n':('1111000','100100','100010','110001','001010','000100'),
't':('0010000','010100','100011','010001','001001','001111'),
'm':('0011110','001001','010001','100011','010100','001000'),

}
		else:
			self.chars = charset


# Arrow codes:
#	n u m
#	l   r
#   s d t
#
	def show_char(self,char,cl=0):
		colour=self.colour
		if char not in self.chars.keys():
			char='.'
		character=self.chars[char]
		line=self.start_line
		for row in character:
			if line >= self.rows:
				break
			if line < 0:
				line += 1
				continue
			p=cl
			for c in row:
				if c == '1':
					i=self.lines[line]+p
					if i < self.lines[line] + self.cols and i >= self.lines[line]:
						if self.smap:
							self[self.smap[i]]=colour
						else:	
							self[i]=colour
				p += 1
			line += 1
	
	def len_txt(self,text):
		ltxt = 0
		for ch in text:
			ltxt += len(self.chars[ch][0])
		return ltxt
	
	def clear_map(self):
		for l in self.smap:
			self[l]=(0,0,0)
			
	async def _show(self,to_show):
		if self.background is not None:
			self.fill(self.background)
		else:
			self.clear_map()
		string=str(to_show)
		ltxt = self.len_txt(string)
		if ltxt < self.cols + 1:
			if self.just == 'C':
				col = int((self.cols - ltxt)/2) + 1	
			if self.just == 'L':
				col = 1
			if self.just == 'R':
				col = int(self.cols - ltxt)
			if len(string) == 1:
				# if self.background is not None:
					# self.fill(self.background)
				# else:
					# self.clear_map()
				self.show_char(string,col)
			else:
				# if self.background is not None:
					# self.fill(self.background)
				# else:
					# self.clear_map()
				for c in string:
					self.show_char(c,col)
					col += len(self.chars[c][0])
		if ltxt > self.cols:
			await self.scroll(string)
				
	async def scroll(self,text,delay=0.15):
		ltxt = 0
		for ch in text:
			ltxt += len(self.chars[ch][0])
		for i in range(self.cols + 1 + ltxt):
			if self.background is not None:
				self.fill(self.background)
			else:
				self.clear_map()
			cl=0
			for c in text:
				self.show_char(c,(self.cols + 1 - i) + cl)
				cl += len(self.chars[c][0])
			self.write()
			await asyncio.sleep(delay)
	
	async def flash(self,chars,colour=None,*,delay=0.5):
		for c in chars:
			await self.show(c,colour)
			await asyncio.sleep(delay)
	
	async def show_text(self):
		while True:
			if self.text:
				await self._show(self.text)
				self.write()
				self.text=''
			await asyncio.sleep(0.2)
			
	async def show(self,text,colour=None,*,just=None):
		while self.text:
			await asyncio.sleep(0)
		if colour is not None:
			self.colour=colour
		if just is not None:
			if just in ['C','L','R']:
				self.just = just
		self.text=text
		
	def clear(self):
		self.fill((0,0,0))
		self.write()
 

