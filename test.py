import asyncio
import time

async def test():
    while True:
        start = time.ticks_ms()
        for i in range(500):
            await asyncio.sleep_ms(2)
        print(time.ticks_diff(time.ticks_ms(), start), 'msecs')
asyncio.run(test())

