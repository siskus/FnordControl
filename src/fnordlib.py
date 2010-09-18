#!/usr/bin/env python
# -*- coding: utf-8-*-

#         fnordlib
#
# (c) by Markus Müller <siskus@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from serial import Serial, EIGHTBITS, STOPBITS_ONE
from threading import Lock

LIGHTCOUNT = 8
DEBUG = 1

class FnordBus:
    
    con = None
    
    lock = None
    
    red = 0
    green = 0
    blue = 0
    
    lights = None
    
    def __init__(self, serial_port):
        
        self.con = Serial(
            port=serial_port,
            baudrate=19200,
            bytesize=EIGHTBITS,
            stopbits=STOPBITS_ONE
        )
        
        self.con.open()
        
        self.lock = Lock()
        
        lights = []
        
        for x in range(LIGHTCOUNT):
            lights.append(FnordLight(self, x))
            
        self.sync()
        self.stop()
        
    
    def getFnordLight(self, number):
        
        return self.lights[number]
    
    
    def setRGB(self, r, g, b):
        
        if DEBUG:
            print("setRGB1 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.red = r
        self.green = g
        self.blue = b
        
        if DEBUG:
            print("setRGB2 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        
    def getRGB(self):
        
        if DEBUG:
            print("getRGB (%s, %s, %s)") % (self.red, self.green, self.blue)
            
        return (self.red, self.green, self.blue) 
        
        
    def update(self):
        
        if DEBUG:
            print("update (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.fade_rgb(255, self.red, self.green, self.blue)
           
        
    def flush(self):
        
        self.con.flushInput()
        self.con.flushOutput()
         
        
    def sync(self, addr = 0):
        
        self.lock.acquire()
        
        for x in range(15):
            self.con.write( chr(27) )
            
        self.con.write( chr(addr) )
        
        self.flush()
        
        self.lock.release()
        
    
    def zeros(self, count = 8):
        
        for x in range(count):
            self.con.write( chr(0) )
    
        
    def fade_rgb(self, addr, r, g, b, step = 5, delay = 0):
        
        self.lock.acquire()
        
        self.con.write( chr(addr) )
        self.con.write(chr(1) )
        self.con.write( chr(step) )
        self.con.write( chr(delay) )
        self.con.write( chr(r) )
        self.con.write( chr(g) )
        self.con.write( chr(b) )
        self.zeros()
        self.flush()
        
        self.lock.release()
        
        
    def stop(self, addr = 255, fading = 1):
        
        self.lock.acquire()
        
        self.con.write( chr(addr) )
        self.con.write( chr(8) )
        self.con.write( chr(fading) )
        self.zeros(12)
        self.flush()
        
        self.lock.release()
    
    
    def black(self, addr = 255):
        
        self.fade_rgb(addr, 0, 0, 0)
        
        
        
class FnordLight():
    
    fnordcontroller = None
    number = 255
    
    red = 0
    green = 0
    blue = 0
    
    
    def __init__(self, fnordcontroller, number):
        
        self.fnordcontroller = fnordcontroller
        self.number = number


    def black(self):
        
        self.fnordcontroller.black(self.number)
        
        
    def setRGB(self, r, g, b):
        
        self.red = r
        self.green = g
        self.blue = b
        
        
    def getRGB(self):
        
        return (self.red, self.green, self.blue) 
        
        
    def update(self):
        
        self.fnordcontroller.fade_rgb(self.number, self.red, self.green, self.blue)
        
        
    def fade_rgb(self, addr, r, g, b, step = 5, delay = 0):

        self.fnordcontroller.fade_rgb(self.number, r, g, b, step, delay)
