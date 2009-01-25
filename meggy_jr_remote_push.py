# meggy_jr_remote_push.py
#
# Python script to serve Meggy Jr. RBG loaded with v1.3 of MeggyJr_RemoteDraw Arduino software
# http://code.google.com/p/meggy-jr-rgb/source/browse/trunk/trunk/arduinolib/meggyjr/examples/SerialCommunication/MeggyJr_RemoteDraw
#
# Version 0.1 1/24/2009
# Copyright (c) 2009 Joshua Ruihley. All rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

import sys
import serial
import time
import urllib2
 
DEBUG = True
GRID_URL = "http://eleventy6.com/openambi/meggy_grid/get_grid.php"

def get_web_grid(GRID_URL):
    grid_response = urllib2.urlopen(GRID_URL)
    grid_txt = grid_response.read()
    grid_buffer = grid_txt.split(',')
    return grid_buffer

# prints only if DEBUG global is set to True
def debug_print(output):
    if DEBUG == True:
	print(output)
    return

# sends serial command to meggy jr to set binary leds to value of bin_value (currently unused)
def set_binary_leds(ser,bin_value):
    cmd = "a%sA\n" % chr(bin_value)
    ser.write(cmd)
    debug_print("Binary LED value set to %s" % bin_value)
    return

# sends command to meggy jr to set pixel x,y with color clr
def set_pixel(ser,x,y,clr):
    cmd = "d%s%s%sD\n" % (chr(x), chr(y), chr(clr))
    ser.write(cmd)
    debug_print("Pixel %s,%s set to color %s" % (x,y,clr))
    return

try:
    ser = serial.Serial('/dev/tty.usbserial-FTE0T664') #establishes 9600,8,N,1 connection to serial port--enter your port here
    debug_print("Success: Serial connection established")
except:
    debug_print("Error: Cannot establish serial connection")
    sys.exit()
    
# delay two seconds to establish serial connection
time.sleep(2.0)

while True:
    try:
        #loop through grid_buffer and send command to Meggy Jr to set pixel
        grid_buffer = get_web_grid(GRID_URL)
        for i in range(0,64):
            x = int(i/8)
            y = i % 8
            clr = int(grid_buffer[i])
            set_pixel(ser,x,y,clr)
            if ser.inWaiting() > 0:
                #output and flush serial input from Meggy Jr
                debug_print("%s:%s" % (ser.inWaiting(), ser.read(ser.inWaiting())))
                ser.flushInput()
    except:
        debug_print("Error: cannot establish connection to server")
    
    #delay two seconds before next call to server
    time.sleep(2.0) 