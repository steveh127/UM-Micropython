import framebuf2, gc
import SQUiXL
from time import sleep_ms
import math

# The SQUiXL library now supports context managers, so we now intitialise the library using a with block, which will automatically deinit() the LCD peripheral when you exit back to the REPL.

# This means no hard reset or even soft reset is required between stopping and re-starting your code.

with SQUiXL as SQUiXL:
	buf = SQUiXL.create_display()

	SQUiXL.screen_init_spi_bitbanged()

	fb = framebuf2.FrameBuffer(buf, 480, 480, framebuf2.RGB565)
	fb.fill(0x2112)
	fb.large_text("SQUiXL!", 100, 50,2, 0xf800)
	fb.ellipse(180, 200, 40, 50, 0x0, True)
	fb.ellipse(190, 190, 20, 20, 0xffff, True)
	fb.ellipse(300, 200, 40, 50, 0x0, True)
	fb.ellipse(310, 190, 20, 20, 0xffff, True)
	fb.ellipse(240, 240, 150, 150, 0xffff)
	fb.rect(190, 320, 100, 20, 0xffff, False)

	fb.text("RED", 100, 400, 0xf800)
	fb.text("GREEN", 200, 400, 0x07e0)
	fb.text("BLUE", 300, 400, 0x001f)

	while True:
		n, points = SQUiXL.touch.read_points()
		for i in range(0, n):
			print(f"id {points[i][3]} x {points[i][0]} y {points[i][1]} size {points[i][2]}")
		sleep_ms(100)
