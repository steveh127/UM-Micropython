# Micropython on SQUiXL.

It is assumed anyone wishing to run micropython on SQUiXL already has familiarity with micropython on the ESP32. SQUiXL is probaly not a good place to start with micropython as the hardware configuration is 'interesting' with the need to drive a large full colour touchscreen. It is assumed esptool, mpremote and Thonny are available.

I develop using a Linux setup, specifically the geany editor setup to use mpremote to copy files to the MCU and run code directly. To annoy Thonny I always ident my code out with tabs not spaces; Micropython is space limited so why waste all those bytes? 

## Installing Micropython.

The first thing to do is to install micropython on the SQUiXL. To do this follow the instructions provided by [Unexpected Maker(UM)in his github repository](https://github.com/UnexpectedMaker/SQUiXL/tree/main/firmware). It is vital to use the firmware provided by UM as it contains the drivers required to run SQUiXL. Check you have a REPL using mpremote then procede to:
 
 
## Installing SQUIXL tools and display demonstration.

This is very basic as this is early development work with no actual applications available yet.

Simply copy all the files, except this one, in the base SQUiXL directory onto the SQUIXL then edit config.py to add your SSID and password - a web based wifi setup comiing soon. 

From the REPL 'import display' will bring up the demonstration screen with a variety of widgets that do a selection of actions.

Also copy down all the fonts in the fonts directory. Lots of them and in any real application a subset will be fine. Any free ttf font can be converted to use with micropython framebuffer based displays using the tools in the microfont directory.

Lots of files:

### Files Provided by UM:

#### drv2605.py

The driver for the haptic device (buzzer)
#### SQUiXL.py  

Contains code to initialise the screen and most of the other connected devices. This changes a lot, the version in my directory works with my code. It is unmodified UM code but may not be the latest version.

### Font Tools:

#### mycrofont.py 
This is a slightly modified version of [microfont.py](https://github.com/antirez/microfont) an excellent module that enables the use of fonts of any size with rotation and multi line strings possible. 

My minor modification is to enable filling in characters with background so overwriting is possible cleanly. This is because the SQUiXL screen reflects changes in the framebuffer immediately with no 'show' so you can't make multiple updates to the framebuffer then display it. Both simple and complicated at the same time.

#### *.mfnt 
A collection of fonts both Serif (LibreBaskerville) and SansSerif(SansLibre). Both in a selection of sizes with Regular, Italic and Bold forms. Excessive for any real application but fine for testing.

#### fonts.py 

Creates microfont objects for each font, also specifies a selection of colours. A module I always import using 'import fonts *' - it's just a list of fonts and colours that several other modules need.

### My 'SQUiXL drivers':

These are the lower level files providing the tools to run applications on the SQUiXL. They utilise asyncio extensively.

#### config.py

This needs editing to add your SSID and password, it also contains clock settings, an offset from GMT and 12 or 24 hr. High on the to do list is to add a web interface to do this. I have the code just needs copying and integrating.

#### squixl_screen.py

This contains two modules SQ_Touch.py, and _SQUiXL_TEXT.py.

SQ_Touch is used to create touchable areas, check for touches and take required actions, each touch area has a seperate asyncio task checking for a touch so simultaneous touches are possible.

_SQUiXL_Text provides screen handling particularly for text but basic framebuffer actions are also available. See code for details, it's quite a small class. It's an _ class as it shouldn't be used directly. 

On importing the module an instance called 'screen' is created. This can then be imported by any number of other processes and only a single 'screen' is used.

#### squixl_time.py

This is used to create a textual clock display in any location, any colour or any font. It uses the network to set time so config.py must be edited for it to run.

#### sq_controls.py

Creates named widgets to display - buttons, select buttons, radio buttons and a menu. To work how I want to I have created my own widget set which I'll expand as needed. All must be named as it's the widgets name that controls it's action.

### The Application Files:

Two files that define the application. At least two are needed but other modules may be used as joke.py is in this demonstration

#### display.py

Basically a coroutine that sets up the screen and adds text and widgets to the screen. Must end with a While True: loop.

Also runs the coroutine - this is the main program and as such can be called anything.

#### actions.py

This is a function that ties the name of a widget to it's actions. If necessary widgets can be given additional properties as actions has access to the widget option. See code for examples. This where the program does it's work. All actions are coroutines for maximum flexibility.

#### joke.py & mrequests.py

mrequests.py is used by jokes.py to download jokes to prove micropython can tell jokes too (currently a limited set per run}