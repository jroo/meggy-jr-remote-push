# meggyjrserial.py
#
# Python class to draw to Meggy Jr. RBG via serial
#
# compatible with v1.3 of MeggyJr_RemoteDraw.pde Arduino software
# http://code.google.com/p/meggy-jr-rgb/source/browse/trunk/trunk/arduinolib/meggyjr/examples/SerialCommunication/MeggyJr_RemoteDraw
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
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

import serial

class MeggyJrSerial:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port)
	
    def open(self):
        self.ser.open()
        return

    def close(self):
        self.ser.close()
        return

    def write(self, cmd):
        self.ser.write(cmd)
        return

    # sends serial command to Meggy Jr to set binary LEDs 
    def set_binary_leds(self,bin_value):
        cmd = "a%sA\n" % chr(bin_value)
        self.ser.write(cmd)
        return

    # sends command to meggy jr to set pixel x,y with pixel_color
    def set_pixel(self, x, y, color):
        cmd = "d%s%s%sD\n" % (chr(x), chr(y), chr(color))
        self.ser.write(cmd)
        return

    # sends commands to meggy jr to set all pixels on grid to values in 
    # grid_buffer list
    def set_grid(self, grid_buffer):
        for i in range(0,64):
            x = int(i/8)
            y = i % 8
            clr = int(grid_buffer[i])
            self.set_pixel(x,y,clr)
            if self.ser.inWaiting() > 0:
                #flush serial input from Meggy Jr
                self.ser.flushInput()