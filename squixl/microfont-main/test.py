from microfont import MicroFont
import framebuf
import SQUiXL as squixl
from time import sleep

RED = 0xf800
GREEN = 0x07e0
BLUE = 0x001f
WHITE = 0xffff
BLACK = 0

with squixl as squixl:
	buf = squixl.create_display()
	bgrnd = 0x000b
	squixl.screen_init_spi_bitbanged()
	fb_width = fb_height = 480
	fb = framebuf.FrameBuffer(buf, fb_width, fb_height, framebuf.RGB565)

	fb.fill(bgrnd)

	x = y = 100

	sans24 = MicroFont("Sans:R:24.mfnt",cache_index=True)
	sans18B = MicroFont("Sans:B:18.mfnt",cache_index=True)
	sans32I = MicroFont("Sans:I:32.mfnt",cache_index=True)
	sans64B = MicroFont("Sans:B:64.mfnt",cache_index=True)
	lb24 = MicroFont("LBask:R:24.mfnt",cache_index=True)
	lb32B = MicroFont("LBask:B:32.mfnt",cache_index=True)
	lb64I = MicroFont("LBask:I:64.mfnt",cache_index=True)

	#framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)

	lb64I.write("SQUiXL !",fb,framebuf.RGB565, fb_width, fb_height, x, y, RED)

	sans24.write("Testing 1 2 3", fb, framebuf.RGB565, fb_width, fb_height, 100, 200, GREEN,rot=45)

	lb32B.write("Going, going, gone...", fb, framebuf.RGB565, fb_width, fb_height, 100, 300, BLUE,rot=-30)

	sans64B.write("Tiddley Pom", fb, framebuf.RGB565, fb_width, fb_height, 100, 360, BLACK)
	
	i = 1
	while True:
		lb32B.write(str(i),fb,framebuf.RGB565, fb_width, fb_height, 10, 10, RED)
		sleep(0.1)
		lb32B.write(str(i),fb,framebuf.RGB565, fb_width, fb_height, 10, 10, bgrnd)
		i += 1
