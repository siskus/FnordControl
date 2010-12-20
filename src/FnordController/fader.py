#!/usr/bin/env python
# -*- coding: utf-8-*-

#         FnordFader
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

import sys

import random
from math import floor, ceil

sys.path.append('..');

from FnordLib import WorkerBase


#===============================================================================
# FnordFaderBase
# This is a solution for a rather specific problem. If you want to fade between
# some specific colors in an easy way, then is FnordFader the solution for your
# Problem.
# You can add as many colors as you like and FnordFader will interpolate
# between them in the interval [0-1]. 
#===============================================================================
class FnordFaderBase(WorkerBase):
    
#    colors = None
#    delay = 0
#    step = 0
#    jitter = 0
#    running = 0
#    wait_factor = 0
    
    def __init__(self, lights):
        WorkerBase.__init__(self, lights)
        self.colors = []
        
        
    def setSpeed(self, speed):
        
        self.speed = speed
       
        
    def addColor(self, color):
        self.colors.append(color)
        
        
    #===========================================================================
    # getColor
    # If no value is specified then a value is randomly choosen.
    #===========================================================================
    def getColor(self, value = -1):
        
        if value == -1 or value < 0.0 or value > 1.0:
            value = random.random()
        
        position = value * (len(self.colors) - 1)
        
        lower = int( floor(position) )
        upper = int( ceil(position) )
        amount = position - lower
        
        lred, lgreen, lblue = self.colors[lower]
        hred, hgreen, hblue = self.colors[upper]
        
        red = int( lred * amount + hred * (1 - amount) )
        green = int( lgreen * amount + hgreen * (1 - amount) )
        blue = int( lblue * amount + hblue * (1 - amount) )
        
        return (red, green, blue)
    
    
    def getStep(self):
        
        return self.step
    
    
    def getDelay(self):
        
        return self.delay
    
    
    def getJitter(self):
                
        return self.jitter
    
    
    def setJitter(self):
        
        return self.jitter
        
    
    def setStep(self, step):
   
        self.step = step
        
    
    def setDelay(self, delay):
        
        self.delay = delay
    
        
class FnordFaderArray(FnordFaderBase):
    
    def __init__(self, lights):
        FnordFaderBase.__init__(self, lights)
        
        
    def run(self):
        
        self.enable()
        
        while self.running:
            
            for item in self.lights:
            
                r, g, b = self.getColor()
                
                item.fade_rgb(r, g, b, self.step, self.delay)
                
            self.wait(0.5)
                
            
class FnordFaderSingle(FnordFaderArray):
    
    def __init__(self, light, fader):
        lights = []
        lights.append(light)
        FnordFaderArray.__init__(self, lights, fader)
    