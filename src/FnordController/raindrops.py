#!/usr/bin/env python
# -*- coding: utf-8-*-

#         Raindrops
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
from FnordLib import WorkerBase, FnordHelper, FnordCluster

import random
from math import floor
from time import sleep


class Raindrops(WorkerBase):
    
        
    def __init__(self, lights, mode):
        WorkerBase.__init__(self, lights)
        self.helper = FnordHelper()
        self.mode = mode
        
        
    def selectOrigin(self):
        
        origin = random.randint(0, self.light_count - 1)
        
        return origin
    
        
    def run(self):
        
        self.enable()
        
        while self.running:        
            
            if self.mode == 1:
                
                nr_of_lights = random.randint(1, 3)
                
                lights = []
                
                # Select the lights, but not the same light twice
                for i in range(nr_of_lights):
                    
                    needNewLight = True
                    
                    while needNewLight:
                        
                        light = self.lights[self.selectOrigin()]
                        
                        try:
                            lights.index(light)
                            #Bad, the list contains the light
                            needNewLight = True
                        except:
                            # Good, the light is not alreay in the list
                            
                            needNewLight = False
                            
                    lights.append(light)  
                        
                
                for light in lights:
                    
                    # Turn on light
                    r, g, b = self.helper.getRandomColor()
                    r, g, b = self.helper.getMaxBright(r, g, b)
                    
                    light.fade_rgb(r, g, b, 50, 0)
                    
                sleep(0.05)
                #self.wait(0.05)
                
                for light in lights:
                    # Fade the light totally
                    light.fade_rgb(0, 0, 0, 2, 0)
                    
                #sleep(0.5)
                self.wait(0.125)
                
            elif self.mode == 2:

                mylights = []
                
                cluster1 = FnordCluster()
                cluster1.registerLight(self.lights[3])
                cluster1.registerLight(self.lights[5])
                
                cluster2 = FnordCluster()
                cluster2.registerLight(self.lights[2])
                cluster2.registerLight(self.lights[6])
                
                cluster3 = FnordCluster()
                cluster3.registerLight(self.lights[1])
                cluster3.registerLight(self.lights[7])
                
                cluster4 = FnordCluster()
                cluster4.registerLight(self.lights[0])
                cluster4.registerLight(self.lights[8])
                
                mylights.append(self.lights[4])
                mylights.append(cluster1)
                mylights.append(cluster2)
                mylights.append(cluster3)
                mylights.append(cluster4)
                 
                
                for light in mylights:
                    
                    if not self.running:
                        break
                
                    # Turn on light
                    r, g, b = self.helper.getRandomColor()
                    r, g, b = self.helper.getMaxBright(r, g, b)
                    
                    light.fade_rgb(r, g, b, 50, 0)
                    
                    sleep(0.05)
                    #self.wait(0.05)
                    
                    # Fade the light totally
                    light.fade_rgb(0, 0, 0, 2, 1)
                    
                    #sleep(0.5)
                    self.wait(0.75, False)
