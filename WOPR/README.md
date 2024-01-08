# Micropython WOPR Web Link

An application to drive Unexpected Makers WOPR via a web interface.

All testing and development has been done using Linux. Windows and Mac users 
should be able to make appropriate modifications to get things going.

This software, while an application as it stands, is intended as a framework
to be modified for more specific applications.

## Installation

First install an up-to-date version of micropython for whatever MCU
you are using following instructions on the micropython download pages. 
The installation has been tested with, and build scripts are available 
for UM Tiny S2 and S3 boards.

The clone these UM-Micropython directories from Github:  [https://github.com/steveh127/UM-Micropython](https://github.com/steveh127/UM-Micropython)
This will include the Bling! software, the bling directory but not common 
can safely be deleted if not required.

You will need mpremote installed as the build scripts require it. Also
strongly recommended as basic development tool when working with 
micropython. (_pip install mpremote_)

Navigate to the WOPR directory and with the WOPR connected run the appropriate
bash build script. (*./builder_S3 or S2*) The build script will need to be 
set as exectable.

## Setup

Reboot the WOPR and you should see the IP address 192.168.4.1 displayed.

Go to WiFi connections on any suitable device, an Android Phone or Tablet 
are fine and you should see, under Networks available 'WOPR'. Connect to this
network, it needs no password and provides no internet connections. It is connecting
to a web server running on the WOPR. On connecting it may well tell you it is
not connected to the internet nor is it secure. You will only connect briefly
so security should not be an issue:

Now open you favourite browser on the device connected to WOPR and enter the IP
address shown on the WOPR(192.168.4.1).

This should bring up a web page. An attempt is made to detect your WiFi 
network and display the SSID, if it is incorrect edit the SSID field. Fill in
the password field. Select other options as appropriate. Daylight saving option
only works if there is no UTC offset (software written in UK, GMT = UTC).

Once settings are correct press 'Save Setup' button. The WOPR should say 
'RESTART NOW'. Do so. You should find whatever you used to connect to WOPR is
now back to your local network. If not manually reconnect it.

On restarting you should see an IP address and get a beep if the optional audio shield
is present.

Should you not see an IP address or you wish to reconfigure the network you will need to copy
the net_config.py file in the common directory onto the MCU and reboot. This
will restart the setup procedure. 

## Usage

To show time press the right button on the front of the WOPR, the right button will
then toggle time display. The left button brings up the IP address. 

There are 2 small buttons behind the left end of the WOPR, the upper button(3) toggles 
daylight saving, the lower button(4) toggles 24 / 12 hour clock. Setting changes are permanent
and will survive rebooting.


Again with your favourite browser, on any device connected to your local network, enter the
displayed IP address into the address field. This brings up the WOPR website giving control of
all features of the WOPR with a messaging facility. Clock settings changed will be retained. 

## Technical Notes

The objective of this section is to indicate something of the structure of the program and to
indicate where customisations may readily be made.

### *web_link.py* This is the main driver file for the program, imported by *main.py*. It contains the
subroutines to manage webpages, linking form actions to actual actions. This is commented to
indicate the application specific areas that can be modified. The format of the imports is
important, *get_WOPR* is a function that delivers a unique instances of the WOPR control class. The
*web_pages* links is dictionary of links used to aid creation of web pages dynamically. *async def main()* sets
up the WOPR software and creates all necessary tasks, these can be modified as necessary. 
Finaly it initiates an endless asyncio loop. If there is no SSID defined then an alternative program, *net_setup.py* 
is imported. This is essentially a version of *web_link.py* to run the network setup web page with it's own set
of files. It is only imported if needed.


 
