#!/usr/bin/env python
# -*- coding: utf-8-*-

#         XMas
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

sys.path.append('..');
from FnordLib import WorkerBase
from math import floor
import random
from time import sleep


class XMas(WorkerBase):
    
        
    def __init__(self, lights):
        WorkerBase.__init__(self, lights)
        
        self.step = 20
        
        self.colors = []
        
        # Defining colors
        self.colors.append( (255, 000, 000) )
        self.colors.append( (000, 255, 000) )
        self.colors.append( (050, 050, 255) )
        self.colors.append( (255, 000, 255) )
        self.colors.append( (255, 255, 000) )


    def getRandomColorIndex(self):
        
        value = int( floor( random.random() * len(self.colors) ) )
        
        return value
    

    def run(self):
        
        last_color = self.getRandomColorIndex()
        
        for light in self.lights:
            
            color = self.getRandomColorIndex()
            
            while color == last_color:
                
                print("Error: Got the same color")
                color = self.getRandomColorIndex()
            
            print("Setting color: %s" % color)
            
            r, g, b = self.colors[color]
            
            light.fade_rgb(r, g, b, self.step, self.delay)
            
            last_color = color
            
        self.sleep(25)
        
        for light in self.lights:
            
            light.fade_rgb(0, 0, 0, self.step, self.delay)
            
        self.wait(5)
        
        
            