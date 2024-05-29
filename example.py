#!/usr/bin/env python3
##############################
# Example Script for using this package
#----------------------------------------
#
# 1. Initialize the Virtual Environment before using this file.
#
# python3 -m venv venv
#
# 2. Activate and install the Dependencies:
#
# source ./venv/bin/activate
# pip3 install -r requirements.txt
#
##############################

###
# Imports
from W7500isp import ispcmd
import serial

###
# Parameters
PORT='/dev/ttyUSB0'
BAUD=460800
FNAME='firmware.bin'

###
# Main Program
print('Starting comm on ' + PORT + '@ ' + str(BAUD))

# Added Timeout for faster Eject in case the boot fails
comport = serial.Serial(PORT, BAUD, timeout=1)
isp = ispcmd.ispcmd(comport)

# Check is the Boot mode is ready
isp.checkisp()

print(' Lock Flags:')
print(isp.readLockFlag())

print(' Erase All Flash:')
isp.eraseFlashAll()

print(' Programming Flash with ' + FNAME + '\n');
isp.downloadDataByXModem( FNAME, 'code' )

# Reset the MCU to start the Program
isp.resetSystem()

# Finally close port and Exit
comport.close()
