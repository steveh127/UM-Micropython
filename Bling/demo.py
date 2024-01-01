import asyncio
from machine import Pin
from random import randint

from bling import Bling_Display,Bling_Buttons

display=Bling_Display()

async def random_bar_graph():
	display.scrolling=False
	colours=('{BLUE}','{RED}','{GREEN}','{YELLOW}','{PURPLE}','{WHITE}')
	display.gap=1
	while not display.text and not display.scrolling:
		await display.bar_chart( 
		                  (randint(0,100),),
		                  (randint(0,100),colours[randint(0,5)]),
		                  (randint(0,100),colours[randint(0,5)]),
		                  (randint(0,100),colours[randint(0,5)]),
		                  (randint(0,100),colours[randint(0,5)]),
		                  [randint(0,100)],
		                  high=100,
		                  pre='>',
		                  post='1'
		                )
		for _ in range(100):
			if display.text or display.scrolling:
				break
			await asyncio.sleep_ms(10)

async def b0():
	asyncio.create_task(random_bar_graph())
	await asyncio.sleep(0.3)
		
async def b1():
	await display.show('{NO GAP}Button{GAP} {RED}1|',colour=display.GREEN(3),justify=('L'))
	
async def b2():
	await display.show('{RED}1{GREEN}23{BLUE}{NO GAP}45{WHITE}678{NO GAP}{RED}9&{YELLOW}1{GREEN}23{PURPLE}45',brightness=3)
	
async def b3():
	if display.background == display.BLACK(1):
		display.set_background(display.BLUE(1))
	else:
		display.set_background(display.BLACK(1))
	await asyncio.sleep(0.3)

async def main():
	buttons=Bling_Buttons([b0,b1,b2,b3])
	display.setup_tasks()
	asyncio.create_task(buttons.check())
	await display.show('{RED}Testing {BLUE}{NO GAP}123{GREEN}{GAP}4 5 6 ',brightness=3)
	while True:
		await asyncio.sleep(5)
	
asyncio.run(main())
	

			
