# Micropython WOPR Web Link

An application to drive [Unexpected Makers WOPR](https://unexpectedmaker.com/shop.html#!/W-O-P-R-Display-Kit/p/578899083/) via a web interface.

All testing and development has been done using Linux. Windows and Mac users 
should be able to make appropriate modifications to get things going.

This software, while an application as it stands, is intended as a framework
to be modified for more specific applications. As far as I am concerned this is 
a completed piece of work and I don't intend developing it further. Feel free to
clone and modify the code as much as you like.

## Installation

First install an up-to-date version of micropython for whatever MCU
you are using following instructions on the micropython download pages. 
The installation has been tested with, and build scripts are available 
for UM Tiny S2, S3 and Tiny Pico boards.

Then clone the UM-Micropython directories from Github:  [https://github.com/steveh127/UM-Micropython](https://github.com/steveh127/UM-Micropython)
This will include the Bling! software, the bling directory but not common 
can safely be deleted if not required.

You will need mpremote installed as the build scripts require it. Also
strongly recommended as basic development tool when working with 
micropython. (_pip install mpremote_)

Navigate to the WOPR directory and with the WOPR connected run the appropriate
bash build script. (*./builder_S3, builder_S2 or builder_tp*) The build script will need to be 
set as executable.

## Setup

Reboot the WOPR and you should see the IP address 192.168.4.1 displayed.

Go to WiFi connections on any suitable device, an Android Phone or Tablet 
are fine and you should see, under Networks available 'ORAC' (ORAC is another fictional
computer that should be familiar to fans of 70's UK SCi-Fi). Connect to this
network, it needs no password and provides no internet connections. It is connecting
to a web server running on the WOPR. On connecting it may well tell you it is
not connected to the internet nor is it secure. You will only connect briefly
so security should not be an issue:

Now open you favourite browser on the device connected to WOPR and enter the IP
address shown on the WOPR(192.168.4.1).

This should bring up a web page. An attempt is made to detect your WiFi 
network and display the SSID, if it is incorrect edit the SSID field. Fill in
the password field. Select other options as appropriate. Daylight saving option
only works if there is no UTC offset (software written in UK so GMT = UTC).

Once settings are correct press 'Save Setup' button. The WOPR should say 
'RESTART NOW'. Do so. You should find whatever you used to connect to WOPR is
now back to your local network. If not manually reconnect it.

On restarting you should see an IP address and get a beep if the optional audio shield
is present.

Should the WOPR fail to connect to the network after trying for about a minute there will
be a 'NO NETWORK REBOOT NOW' message. On rebooting repeat setup procedure above. 

## Usage

To show time press the right button on the front of the WOPR, the right button will
then toggle time display. The left button brings up the IP address. 

There are 2 small buttons behind the left end of the WOPR, the upper button(3) toggles 
daylight saving, the lower button(4) toggles 24 / 12 hour clock. Setting changes are permanent
and will survive rebooting.


Again with your favourite browser, on any device connected to your local network, enter the
displayed IP address into the address field. This brings up the WOPRs website giving control of
all features of the WOPR with a messaging facility. Clock settings changed will be retained. 

## Technical Notes

The objective of this section is to indicate something of the structure of the program and to
indicate where customisations may readily be made.

### *web_link.py* 

This is the main driver file for the program, imported by *main.py*. It contains the
subroutines to manage webpages, linking form actions to actual actions. This is commented to
indicate the application specific areas that can be modified. The format of the imports is
important, *get_WOPR* is a function that delivers a unique instances of the WOPR control class. The
*web_pages* links is dictionary of links used to aid creation of web pages dynamically. __*async def main()*__ sets
up the WOPR software and creates all necessary tasks, these should be modified as necessary. 
Finaly *async def main()* initiates an endless asyncio loop. 

If there is no SSID defined in *net_config.py* then an alternative program, *net_setup.py* 
is imported. This is essentially a version of *web_link.py*  that creates its own access point to run 
the network setup web page with its own set of files. It is only imported if needed.

#### *socket_simple*

This is used by *web_link.py* to create a socket, connecting to the network if necessary. It uses *asyncio* coroutines
to listen for connections and take a supplied action on receiving a connection. The network connection will set the
socket status to either 'connected' or 'disconnected'. It will try for about a minute to connect. This status should
be checked before trying to use the socket.

### *wopr_as.py*

This creates the software to drive the hardware. It consists of two classes, the main WOPR class and a supporting 
RGB class used to manage the 5 LEDs on the WOPR. An instance of the WOPR class with a basic asyncio driver and a network
connection will act as a standalone program, as it is only controlling the clock and displaying IP address. The network is
only neede by WOPR to set the clock. The *active_WOPR* closure is used to create a function, *get_WOPR* that delivers a 
singleton instance of WOPR. This simplifies accessing WOPR from both *web_link* and the *actions* class that links WOPR with
web controls. Adding additional functionality should be fairly straigtforward, an obvious possibility is adding alarm or
timer functions. It certainly be possible to simulate the original WOPR from the movie *War Games*. It is also possible, 
as some spare pins are broken out, to connect to additional hardware such as sensors or motors. This software could also act a
framework to connect to different hardware - anything with LEDs, buttons and a display will need similiar functionality. The
only board specific file is *board.py* which provides pin mappings for the RGB LEDS, buzzer and buttons. The I2C interface is
common across the Unexpected Maker boards compatible with WOPR.

#### *led_multi_as.py*

The WOPR display consists of twelve 14 segment LED arrays that provide an attractive, if retro, display. They are driven,
via an I2C interface, by three HT16K33 chips. The micropython driver for these chips provides basic access which the LED_Multi_AS
class provides higher level functionality such as a character set and *asyncio* display routines. There are different ways
the LEDs can be connected to the chips so the character set is vendor dependent. The mapping here, shown in comments in module,
works for both WOPR and for similiar Adafruit 4 LED displays but apparently identical Sparkfun displays have a radically different
mapping. The obvious practical tweaks here are to modify or extend the character set. For further details see comments in module.   
 
### *web_pages.py* & *setup_pages.py*

These modules define the web pages created dynamically for display and the actions to be performed. The classes used for this
are set up in the *web_builder.py* module. Don't expect to create anything too complex, this is about using web pages for
'dashboard' control of devices. The basic structure for a web page is a title, a body, an action map, and a CSS file, here *dash.css*. 
The body contains a display list and a form, both the latter consist primarily of lists of widgets. The *web_pages* used to control
WOPR have examples of all the widgets available. Using the WOPR pages as a template it shouldn't be too dificult to create new
web pages. The actions driven by the forms are defined in the *actions.py* module, see below. Note that forms can either have a 
single, possibly complex, action with a single submit button that delivers all form fields or can have a set of submit buttons 
for each widget to do specific actions. The *setup_pages* uses a single button to save the defined configuration parameters while 
*web_pages* has seperate submit buttons for each widget. The final element in the web_pages module is a dictionary of links that
connects link names to web_page classes. This must include a 'home' link name. This is imported by *web_link* to control web
page generation. Note that web_pages and web_builder and the parts of web_link not associated with WOPR are pure Python and run
just fine on standard Python (3.x), initial development was done on Linux. It is also worth noting that the *net_setup*,
*setup_pages* have no links to WOPR and can be run independently, *setup_actions* will need modifying to display appropriate 
messages to the display.

#### *dash.css*

This is a perfectly standard CSS file and can be modified as required, if necessary widgets can have an ID defined. Strictly 
speaking there's no cascading going on, the style is simply embedded in the header of each web_page.


#### *actions.py* & *setup_actions.py*
 
These modules link the web page form widget actions to the underlying hardware. The format is fairly simple, each action method must 
have the arguments *(self,values)*, even if no values are generated. Methods to simply deliver information for use in form fields
are also possible. See module files for examples; they are used to populate form fields with current values for example.

 
### Security

The build includes a *net_config.py* file that contains local network parameters in clear text. Anyone with minimal micropython 
skills and access to the hardware could read this file. 
