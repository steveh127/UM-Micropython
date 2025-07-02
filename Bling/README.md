# Unexpected Makers - Bling! 
## Micropython 

Bling! features an 8 x 40 RGB LED array that can be controlled using the micropython(MP) NeoPixel 
class included with the standard MP build. The basic Bling! board includes an ESP32 S3 mcu and a lot
of other goodies. [See Unexpected Maker's Bling! webpage for details.](https://unexpectedmaker.com/shop.html#!/BLING/p/596946493// "Bling! Webpage")
There is also an excellent [bling github repository](https://github.com/UnexpectedMaker/bling) which includes
a wealth of information including schematics.

The micropython [Unexpected Maker Tiny S3 micropython build](https://micropython.org/download/UM_TINYS3/) has been 
used for development.

This respository contains:

***bling.py***, a micropython module providing classes to control Bling display and buttons and ***kclock***, a kitchen clock and timer.

## *bling.py* - Tools to use with Bling

#### *class Bling_Display.py*

This class manages the display, in particular textual display. A full set of characters is provided which is readily extensible either by editing code or on the fly.

Text can be scrolled, text too long to show completely will be automatically scrolled.

Strings can use markup to change colours within a string e.g. '{RED}B{PURPLE}ling{GREEN}!'`

For the full range of functions see the code.

To function correctly the display should be run in an asynchronous environment. Before initiating the main async loop run the .setup_tasks() function. 

Text should be displayed using the show_string function, optional parameters will set the colour, brightness and justification ('C','R' or 'L') otherwise the current global settings will be used.

There is also a colour class to manage variable brightness of defined colours. 

#### *class Bling_Buttons*

A small class used to setup and check buttons.

When creating an instance - and only create one! Supply a list of four coroutines as the initial actions of the buttons. Actions can be changed during the program running.

A task to run the button check coroutine is essential. 

# *kclock*, a program for a kitchen clock / timer for Bling!.

#### Installation

I use Linux to develop in micropython and a linux script to do the build is provided. Otherwise use mpremote or your preferred tools to copy bling.py and the contents of the kclock directory to the mcu.

Currently it is necessary to edit `net_config.py` to provide SSID and password to connect to your WiFi.

Network is only used to set time.

Note as I live in the UK the UTC provided by ntptime is great as for all practical purposes UTC = GMT. I also have a function to set daylight saving which is only guaranteed to work in the UK. And will probably work in other countries using GMT. Otherwise you will need to tweak the code.

Buttons: upper left is 'Set', upper right is 'Start'. Other buttons available for future enhancements. 

#### Operation

Starts in clock mode. Clock display can be toggled with 'Start' button.

Pressing set enters timer mode showing 00:00

Set button is used to set minutes. Start initiates countdown.
Beeps and flashes at end. Set clears alarm and returns to clock. 
If Set is pressed during count return to clock,

With display zeroed Start initiates stopwatch mode. This counts up until Set is
pressed which holds display. Pressing Set again returns to clock.

Pressing Start when timing pauses timer, can restart timing with Start or return to Clock
with Set. 

### Possible enhancements

As this application relies on the ESP32-S3s accurate internal RTC with time being set using an ntp server and updated daily the I2C pins are freed up and can be used as general GPIO pins to drive, for instance, a buzzer for alarm use. I've tested this and it works fine and doesn't require the complexity of I2S for basic sounds.

Add web interface to input network parameters. Already done for other projects just needs copying across and customising.

Provide support for other timezones.

Add longer term alarm functions with possible web page to control locally.