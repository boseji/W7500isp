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
import argparse
from pathlib import Path

# Get the Commandline definition
parser = argparse.ArgumentParser(
        prog="example.py",
        description="Surf5 Programming example")
# Add Arguments
parser.add_argument("-p", "--port", type=str,
                    help="Serial Port name [/dev/ttyUSB0] (eg. COM1,COM5 or /dev/ttyUSB0, /dev/ttyACM1 etc.)",
                    default='/dev/ttyUSB0')
parser.add_argument("-b", "--baud", type=int,
                    help="Serial BAUD rate [460800] (eg. 57600 or 115200 etc.)",
                    default='460800')
parser.add_argument("file", help="Binary File to be flashed")

args = parser.parse_args()
###
# Parameters
PORT='/dev/ttyUSB0'
if args.port:
    PORT=str(args.port)

BAUD=460800
if args.baud:
    BAUD=int(args.baud)

FNAME='firmware.bin'
if args.file:
    FNAME=str(args.file)
    
# Check the File
target_dir = Path(FNAME).resolve()
if not target_dir.exists():
    print("Error the file supplied does not exist")
    raise SystemExit(1)

# Check Serial Port
target_dir = Path(PORT)
if not target_dir.exists():
    print("Error the Serial Port supplied does not exists")
    raise SystemExit(1)
###
# Main Program
print('Starting comm on ' + PORT + ' @ ' + str(BAUD))
print(FNAME)

# Added Timeout for faster Eject in case the boot fails
comport = serial.Serial(PORT, BAUD, timeout=1)
isp = ispcmd.ispcmd(comport)

# Check if the Boot mode is ready
print("\n\n * Checking for Boot Mode :\n")
print(" (Press the Boot and Reset together, keeping the Boot held release reset)")
print(" (Release boot also once you see the 'Boot Mode Entered' message)\n") 
isp.checkisp()

print('\n * Lock Flags: \n')
isp.readLockFlag()

print('\n * Erase All Flash: \n')
isp.eraseFlashAll()

print('\n * Programming Flash with ' + FNAME + '\n');
isp.downloadDataByXModem( FNAME, 'code' )

# Reset the MCU to start the Program
isp.resetSystem()

# Finally close port and Exit
comport.close()
