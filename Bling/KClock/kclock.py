'''
Kitchen Clock - tested with Seeed XIAO ESP32 C3

'''
from machine import Pin
import uasyncio as asyncio

from clock_timer import ClockTimer

show_time    = TM1637_Time(clk=Pin(6), dio=Pin(7))		
buzzer       = Pin(2,Pin.OUT)

b_set   = Pin(4,Pin.IN,Pin.PULL_UP)
b_start = Pin(5,Pin.IN,Pin.PULL_UP)

clock_timer  = ClockTimer(show_time,rgb=Pin(3),buzzer=Pin(2))

async def main():
	await clock_timer.setup_tasks(b_set,b_start)
	while True:
		await asyncio.sleep(10)

asyncio.run(main())

				


