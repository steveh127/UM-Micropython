
# Unexpected Maker - Light Crystals Kit Puzzle clock
## *A micropython application* 

## Introduction

This application runs a 'puzzle clock' on UMs Light Crystals kit. It displays the time in a number of somewhat cryptic formats and one rather less cryptic form. Exactly how they work is for you to work out.

I put this program together using code from other projects modified slightly. Technical details are provided elsewhere but with care modifying the code should be straightforward if you know micropython and are happy using asyncio. 

## Installing Software

First install micropython on your light crystals kit. Use the Unexpected Maker OMGS3 build as that is what the light crystals kit is based on. 

Linux users can download the repository navigate to the Light_Crystals directory, make clock_builder executable and then run it.

Other users just need to copy the files in the 'build' directory to the mcu using mpremote or whatever tool you usually use to copy files to mcus.

Instructions on setting up the wifi are shown below and are also in instructions.txt which is a basic printable version.

## Setting up the WIFI connection

The Clock needs to make occasional connections to the internet to set the time and ensure it stays correct. For this you need to set the WIFI network name and password.

1. On first powering up the NeoClock the display will be all blue. This shows that there is no network configuration set.

2. Go to WiFi settings on your PC, phone or tablet.

3. On the list of available networks you should see CLOCK. This is a (very) temporary network provided by the NeoClock. It only exists while the WIFI is being set up. Connect to this network, no other network is required. It will may warn of no internet connection, this is normal.

4. Open your favourite web browser and, in the address box, enter:
				   192.168.4.1
5. This should bring up a ‘Clock Dashboard’ with fields for the WIFI, time and shape parameters. It should automatically detect the strongest local network.

6. Carefully enter your correct / required parameters and save them. On clicking the  ‘Save’ button the display should go green.

The clock will soon switch to displayimg time using the 'blocks' style. Once time is set the network disconnects. It will briefly reconnect and reset time twice a day at 10:05 and 20:05.

Note for the UM crystal display using blocks time shows as intended with USB port to left when viewed from front.

This setup only needs doing once. NeoClock remembers WIFI, shape and time parameters.

Should parameters be set incorrectly or the WIFI network  not available NeoClock will try to connect for a while. Eventually the display will briefly go blue and then blank.  Repeat the instructions to reconnect.

Currently NeoClock operates on GMT / BST which change automatically. 

An offset can be set when setting up the clock for non GMT use, if an offset is set then daylight saving won’t be automatically set.

The button nearer the edge cam be used to switch time display formats, the last selected format will be remembered.





