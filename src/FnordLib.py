#!/usr/bin/env python
# -*- coding: utf-8-*-

#         fnordlib
# A collection of classes to control fnordlights on different levels of 
# abstraction
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
import random
from time import sleep

# Number of lights to be accessible on the bus
LIGHTCOUNT = 10

# If true, enable debug outputs
DEBUG = 0


#===============================================================================
# FnordBus
# ========
#
# This is the the most basic abstraction from a FnordNet-Bus with FnordLights
# connected.
# Upon object creation, it will initialize the bus. This means that it will
# instruct the light to stop fading and it sends a sync signal through the
# bus.  
#===============================================================================
class FnordBus:
    
    con = None
    
    lock = None
    
    # These three variables hold a "bus color". The controller has the ability
    # to let all the lights on bus display this color. It is controlled via
    # the appropriate functions (setRGB, getRGB and update)
    red = 0
    green = 0
    blue = 0
    
    lights = None
    
    def __init__(self, serial_port, doReset = True):
        
        self.con = Serial(
            port=serial_port,
            baudrate=19200,
            bytesize=EIGHTBITS,
            stopbits=STOPBITS_ONE
        )
        
        self.con.open()
        
        self.lock = Lock()
        
        self.lights = []
        
        # The controller creates individual FnordLight objects for each
        # FnordLight on the bus
        for x in range(LIGHTCOUNT):
            self.lights.append(FnordLight(self, x))
        
        if doReset:    
            self.reset()
        
        
    #===========================================================================
    # resetBus
    # Resets the bus
    #===========================================================================
    def reset(self):
        
        self.sync()
        self.stop()
        
        
    
    #===========================================================================
    # getFnordLight
    # Returns a specific FnordLight from the bus
    #===========================================================================
    def getFnordLight(self, number):
        
        return self.lights[number]
    
    
    #===========================================================================
    # getFnordLights
    # Returns all FnordLights from the bus
    #===========================================================================
    def getFnordLights(self):
        
        return self.lights
    
    
    #===========================================================================
    # setRGB
    # Sets the "bus color"
    #===========================================================================
    def setRGB(self, r, g, b):
        
        if DEBUG:
            print("setRGB1 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.red = r
        self.green = g
        self.blue = b
        
        if DEBUG:
            print("setRGB2 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        
    #===========================================================================
    # getRGB
    # Return the current "bus color"
    #===========================================================================
    def getRGB(self):
        
        if DEBUG:
            print("getRGB (%s, %s, %s)") % (self.red, self.green, self.blue)
            
        return (self.red, self.green, self.blue) 
        
    
    #===========================================================================
    # update
    # Instructs all FnordLights to fade to the current "bus color"
    #===========================================================================
    def update(self):
        
        if DEBUG:
            print("update (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.fade_rgb(255, self.red, self.green, self.blue)
           
        
        
    #===========================================================================
    # flush
    # Flushes the serial buffer in order to write all the bytes out on the bus.
    #===========================================================================
    def flush(self):
        
        self.con.flushInput()
        self.con.flushOutput()
         
        
    #===========================================================================
    # sync
    # Send a sync signal on the bus
    #===========================================================================
    def sync(self, addr = 0):
        
        self.lock.acquire()
        
        for x in range(15):
            self.con.write( chr(27) )
            
        self.con.write( chr( int(addr) ) )
        
        self.flush()
        
        self.lock.release()
        
    
    #===========================================================================
    # zeros
    # Helper function to send zeros over the wire
    #===========================================================================
    def zeros(self, count = 8):
        
        for x in range( int(count) ):
            self.con.write( chr(0) )
    
        
    #===========================================================================
    # fade_rgb
    # Fade the FnordLight no. addr to the color (r, g, b) with the optional
    # step and delay.
    #===========================================================================
    def fade_rgb(self, addr, r, g, b, step = 5, delay = 0):
        
        self.lock.acquire()
        
        self.con.write( chr( int(addr) ) )
        self.con.write(chr(1) )
        self.con.write( chr( int(step) ) )
        self.con.write( chr( int(delay) ) )
        self.con.write( chr( int(r) ) )
        self.con.write( chr( int(g) ) )
        self.con.write( chr( int(b) ) )
        self.zeros()
        self.flush()
        
        self.lock.release()
        
        
    #===========================================================================
    # stop
    # Stop the fading on the whole bus if no addr is specified.
    #===========================================================================
    def stop(self, addr = 255, fading = 1):
        
        self.lock.acquire()
        
        self.con.write( chr( int(addr) ) )
        self.con.write( chr(8) )
        self.con.write( chr( int(fading) ) )
        self.zeros(12)
        self.flush()
        
        self.lock.release()
        
        
    #===========================================================================
    # start_program
    # Starts a predefined program
    #===========================================================================
    def start_program(self, addr, program, params):
        
        self.lock.acquire()
        
        self.con.write( chr( int(addr) ) )
        self.con.write( chr(7) )
        self.con.write( chr( int(program) ) )
        
        chrcount = 12 - len(params)
        
        for param in params:
            self.con.write( chr( int(param) ) )
            
        self.zeros(chrcount)
        self.flush()
        
        self.lock.release()
    
    
    #===========================================================================
    # black
    # Fades the entire bus to black if no addr is specified.
    #===========================================================================
    def black(self, addr = 255):
        
        self.fade_rgb(addr, 0, 0, 0)

#===============================================================================
# FnordBusDummy
# =============
#
# This is a dummy implementation of a FnordBus for testing purposes
# This is the the most basic abstraction from a FnordNet-Bus with FnordLights
# connected.
# Upon object creation, it will initialize the bus. This means that it will
# instruct the light to stop fading and it sends a sync signal through the
# bus.  
#===============================================================================
class FnordBusDummy:
    
#    con = None
#    
#    lock = None
    
    # These three variables hold a "bus color". The controller has the ability
    # to let all the lights on bus display this color. It is controlled via
    # the appropriate functions (setRGB, getRGB and update)
    red = 0
    green = 0
    blue = 0
    
    lights = None
    
    def __init__(self, serial_port, doReset = True, debug = True):
        
        self.debug = debug
        
        self.con = serial_port
        
        self.lock = Lock()
        
        self.lights = []
        
        # The controller creates individual FnordLight objects for each
        # FnordLight on the bus
        for x in range(LIGHTCOUNT):
            self.lights.append(FnordLight(self, x))
        
        if doReset:    
            self.reset()
        
        
    #===========================================================================
    # resetBus
    # Resets the bus
    #===========================================================================
    def reset(self):
        
        self.sync()
        self.stop()
        
        
    
    #===========================================================================
    # getFnordLight
    # Returns a specific FnordLight from the bus
    #===========================================================================
    def getFnordLight(self, number):
        
        return self.lights[number]
    
    
    #===========================================================================
    # getFnordLights
    # Returns all FnordLights from the bus
    #===========================================================================
    def getFnordLights(self):
        
        return self.lights
    
    
    #===========================================================================
    # setRGB
    # Sets the "bus color"
    #===========================================================================
    def setRGB(self, r, g, b):
        
        if self.debug:
            print("setRGB1 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.red = r
        self.green = g
        self.blue = b
        
        if self.debug:
            print("setRGB2 (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        
    #===========================================================================
    # getRGB
    # Return the current "bus color"
    #===========================================================================
    def getRGB(self):
        
        if self.debug:
            print("getRGB (%s, %s, %s)") % (self.red, self.green, self.blue)
            
        return (self.red, self.green, self.blue) 
        
    
    #===========================================================================
    # update
    # Instructs all FnordLights to fade to the current "bus color"
    #===========================================================================
    def update(self):
        
        if self.debug:
            print("update (%s, %s, %s)") % (self.red, self.green, self.blue)
        
        self.fade_rgb(255, self.red, self.green, self.blue)
           
        
        
    #===========================================================================
    # flush
    # Flushes the serial buffer in order to write all the bytes out on the bus.
    #===========================================================================
    def flush(self):
        
        if self.debug:
            print("flushing...")
         
        
    #===========================================================================
    # sync
    # Send a sync signal on the bus
    #===========================================================================
    def sync(self, addr = 0):
        
        self.lock.acquire()
        
        if self.debug:
            print("Syncing...")
        
        self.flush()
        
        self.lock.release()
        
    
    #===========================================================================
    # zeros
    # Helper function to send zeros over the wire
    #===========================================================================
    def zeros(self, count = 8):
        
        if self.debug:
            print("Writing zeros...")
    
        
    #===========================================================================
    # fade_rgb
    # Fade the FnordLight no. addr to the color (r, g, b) with the optional
    # step and delay.
    #===========================================================================
    def fade_rgb(self, addr, r, g, b, step = 5, delay = 0):
        
        self.lock.acquire()
        
        if self.debug:
            print("fade_rgb: addr:%s r:%s g:%s b:%s step:%s delay:%s" %
                  (addr, r, g, b, step, delay) )
        
        self.zeros()
        self.flush()
        
        self.lock.release()
        
        
    #===========================================================================
    # stop
    # Stop the fading on the whole bus if no addr is specified.
    #===========================================================================
    def stop(self, addr = 255, fading = 1):
        
        self.lock.acquire()
        
        if self.debug:
            print("Stop...")
            
        self.zeros(12)
        self.flush()
        
        self.lock.release()
        
        
    #===========================================================================
    # start_program
    # Starts a predefined program
    #===========================================================================
    def start_program(self, addr, program, params):
        
        self.lock.acquire()
        
        if self.debug:
            print("Starting program %s" % program)
            
        self.zeros(10)
        self.flush()
        
        self.lock.release()
    
    
    #===========================================================================
    # black
    # Fades the entire bus to black if no addr is specified.
    #===========================================================================
    def black(self, addr = 255):
        
        self.fade_rgb(addr, 0, 0, 0)
        
    
        
#===============================================================================
# FnordCluster
# A FnordCluster is a collection of FnordLights grouped together and treated as
# a single FnordLight. As it has the same API as a FnordLight, it is possible 
# to substitute a FnordLight with a FnordCluster without the need to make
# changes in the programming.
#
# It is also possible to add FnordLights or even FnordClusters (since they have
# the same API) to a FnordCluster in order to synchronize several lights.
# 
# Furthermore, you are not limited to lights on the same bus. You can group
# lights from different busses together. 
#===============================================================================
class FnordCluster():
    
    cluster = None
    
#    red = 0
#    green = 0
#    blue = 0
    
    
    def __init__(self):
        self.cluster = []
        
        self.red = 0
        self.green = 0
        self.blue = 0
    
    #===========================================================================
    # registerLight
    # With this function, you can register FnordLights (or FnordClusters)
    #===========================================================================
    def registerLight(self, light):
        
        if DEBUG:
            print("FnordCluster: Register light")
        
        self.cluster.append(light)
        
    #===========================================================================
    # removeLight
    # With this function, you can remove FnordLights (or FnordClusters) from
    # the cluster.
    #==========================================================================
    def removeLight(self, light):
        
        self.cluster.remove(light)
        
        
    def black(self):
        
        for light in self.cluster:
            light.black()
        
        
    def setRGB(self, r, g, b):
        
        self.red = r
        self.green = g
        self.blue = b
        
        
    def getRGB(self):
        
        return (self.red, self.green, self.blue) 
        
        
    def update(self):
        
        for light in self.cluster:
            light.fade_rgb(self.red, self.green, self.blue)
        
        
    def fade_rgb(self, r, g, b, step = 5, delay = 0):
        
        if DEBUG:
            print("FnordCluster: fade_rgb to (%s,%s,%s)" % (r, g, b) )

        for light in self.cluster:
            light.fade_rgb(r, g, b, step, delay)
            
            
    def start_program(self, addr, program, params):
        
        for light in self.cluster:
            light.start_program(addr, program, params)
        
               
# Base class for all FnordWorkers
class WorkerBase():
    
    def __init__(self, lights):
    
        self.speed = 1.0
        self.running = 0
        self.step = 1
        self.delay = 0
        self.wait_factor = 1.0
        self.lights = lights
        self.light_count = len(self.lights)
        self.fnord_helper = FnordHelper()
        
        
    def enable(self):
        
        self.running = 1
    
    
    def disable(self):
        
        self.running = 0     
        
        
    def setSpeed(self, speed):
        
        self.speed = speed
        
                
    def wait(self, time):
        
        sleep( random.random() * time * self.speed )
        
        
    def run(self):
        
        raise Exception("You need to implement run!")        

        
#===============================================================================
# FnordLight
# This is the abstraction of a single FnordLight.
#===============================================================================
class FnordLight():
    
#    fnordcontroller = None
#    number = 255
    
    # Similar to the bus color holds each FnordLight a light color. 
#    red = 0
#    green = 0
#    blue = 0
    
    
    #===========================================================================
    # __init__
    # Each FnordLight holds a reference to its FnordController in order to
    # be able to control itself.
    #===========================================================================
    def __init__(self, fnordcontroller, number):
        
        self.fnordcontroller = fnordcontroller
        self.number = number
        
        self.red = 0
        self.green = 0
        self.blue = 0
        

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
        
        
    def fade_rgb(self, r, g, b, step = 5, delay = 0):
        
        if DEBUG:
            print("FnordLight(%s): fade_rgb (%s,%s,%s)" % (self.number, r, g, b) )

        self.fnordcontroller.fade_rgb(self.number, r, g, b, step, delay)
        
        
    def start_program(self, addr, program, params):
        
        self.fnordcontroller.start_program(self.number, program, params)
        


###############################################################################
# Helper Functions 
###############################################################################        
class FnordHelper():
    
    def getRandomColor(self):
        
        red = int(random.random() * 255)
        green = int(random.random() * 255)
        blue = int(random.random() * 255)
        
        return (red, green, blue)
    
    
