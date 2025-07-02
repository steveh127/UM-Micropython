# Micropython Code for Unexpected Makers devices.

[Unexpected Maker](https://unexpectedmaker.com/shop.html)(UM) produces a variety of interesting devices which are straightforward to program in Micropython. Code is included to manage the displays and provide a web interface to setup WiFi network parameters and, in some cases control the device.

Generally the provided modules are designed as a basis for further development though some basic applications are provided to demonstrate usage.

I develop applications using Linux and Linux scripts are provided to facilitate installing software. Users of proprietary OSs should be able to copy required files to the devices using mpremote without problems though this is not tested by me.

The code in this repository is provided on an as-is basis. Feel free to download or clone it and use it as  source of ideas. Currently only the SQUiXL code is being actively developed. 

The devices in historical sequence are:

## W.O.P.R

A simulation of a computer from the Film wargames see UMs website for details. Actually a rather nice retro display using 14 bit LEDS. A simple clock with a web messaging system is shown. 

## Bling

A display using tiny RGB LEDs controlled using the neopixel module. Driven with an ESP32-S3 and including an I2S amplifier and SD card slot. A kitchen clock application demonstrates some of it's capabilities.

## Light Crystals Kit

An attractive 9 x 9 LED array, again using the neopixel module. A puzzle clock application shows what it can do.

## SQUiXL

A very capable 480 x 480 touch screen display that includes a I2S and I2C interfaces and an SD card slot. Recently released and micropython in active development by me and Unexpected Maker. 

There is also a *common* directory. this holds the core web modules and can be used in many projects.