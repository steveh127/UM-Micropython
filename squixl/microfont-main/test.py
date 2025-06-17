import SQUiXL
from squixl_text import *
		
with SQUiXL as SQUiXL:
	scr = SQUiXL_Text(sans24I)
		
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64B)

	scr.font = sans24I
	scr.write("Testing 1 2 3", 100, 200, GREEN,rotation=45)


	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)

	scr.write("Tiddley Pom",100, 360, WHITE)

	scr.font = serif32B
	i = 1
	while True:
		scr.write(str(i),10, 10, YELLOW)
		sleep(1)
		scr.write(str(i), 10, 10, scr.background)
		i += 1
