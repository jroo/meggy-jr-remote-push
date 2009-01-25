# meggy_jr_remote_push.py
#
# Python script to draw to Meggy Jr. RGB a grid of colors stored on web server
#
# Version 0.1 1/25/2009
# Copyright (c) 2009 Joshua Ruihley. All rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import urllib2
import meggyjrserial

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

try:
    #establishes 9600,8,N,1 connection to serial port--enter your port here
    meggy_conn = meggyjrserial.MeggyJrSerial('/dev/tty.usbserial-FTE0T664')
    debug_print("Success: Serial connection established")
except:
    debug_print("Error: Cannot establish serial connection")
    sys.exit()
    
# delay two seconds to establish serial connection
time.sleep(2.0)

while True:
    try:
        #get grid from web server
        grid_buffer = get_web_grid(GRID_URL)
    except:
        debug_print("Error: cannot establish connection to server")
    
    #send grid to meggy jr
    meggy_conn.set_grid(grid_buffer)
    
    #delay two seconds before refresh
    time.sleep(2.0) 