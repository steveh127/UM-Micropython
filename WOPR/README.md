# Micropython WOPR Web Link

#WOPR

An application to drive Unexpected Makers WOPR via a web interace.

All testing and development has been done using Linux, Windows and Mac users 
should be able to make appropriate modifications to get things going.

## Installation

First install an up-to-date version of micropython for whatever MCU
you are using following instructions on the micropython download pages. 
The installation has been tested with, and build scripts are available 
for UM Tiny S2 and S3 boards.

The clone these UM-Micropython directories from Github:  [https://github.com/steveh127/UM-Micropython](https://github.com/steveh127/UM-Micropython)
This will include the Bling! software, the bling dirctory but not common 
can safely be deleted if not required.

You will need mpremote installed as the build scripts require it. Also
strongly recommended as basic development tool when working with 
micropython. (_pip install mpremote_)

Navigate to the WOPR directory and with the WOPR connected run the appropriate
bash build script. (*./builder_S3 or S2*)

## Setup

