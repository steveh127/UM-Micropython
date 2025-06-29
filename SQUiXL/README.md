# Micropython on SQUiXL.

It is assumed anyone wishing to run micropython on SQUiXL already has familiarity with micropython on the ESP32. SQUiXL is probaly not a good place to start with micropython as the hardware configuration is 'interesting' with the need to drive a large full colour touchscreen. It is assumed esptool, mpremote and Thonny are available.

I develop using a Linux setup, specifically the geany editor setup to use mpremote to copy files to the MCU and run code directly. To annoy Thonny I always ident my code out with tabs not spaces; Micropython is space limited so why waste all those bytes? 

## Installing Micropython.

The first thing to do is to install micropython on the SQUiXL. To do this follow the instructions provided by [Unexpected Maker(UM)in his github repository](https://github.com/UnexpectedMaker/SQUiXL/tree/main/firmware). It is vital to use the firmware provided by UM as it contains the drivers required to run SQUiXL. Check you have a REPL using mpremote then procede to:
 
 
## Installing SQUIXL tools and display demonstration.