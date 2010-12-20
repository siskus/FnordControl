#!/usr/bin/env python
# -*- coding: utf-8-*-

#         Fireworks
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
from math import floor
from time import sleep

sys.path.append('..');

from FnordLib import WorkerBase, FnordHelper


class FireWorks(WorkerBase):
    
    LIGHT_DIVERSITY = 3
    
    
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
    
    
    def selectOrigin(self):
        
        origin = int( floor( random.random() * self.light_count ) )
        
        return origin
    
    
    def spreadLight(self, origin, colors, iteration):
        
        # Part I: Selecting the affected lights
        
        lower_bound = origin - iteration
        
        if lower_bound < 0:
            lower_bound = 0
            
        upper_bound = origin + iteration
        
        if upper_bound >= self.light_count:
            upper_bound = self.light_count - 1
        
        affected_lights = self.lights[lower_bound : upper_bound]
        
        if lower_bound == upper_bound:
            affected_lights.append(self.lights[lower_bound])
            
        # Part II: Turning the lights on
        
        r, g, b = colors
        
        #for light in affected_lights:
        #    light.fade_rgb(r, g, b, 50, 0)
        self.lights[lower_bound].fade_rgb(r, g, b, 50, 0)
        self.lights[upper_bound].fade_rgb(r, g, b, 50, 0)
        
        # Part III: Let the lights slowly fade
        
        for light in affected_lights:
            
            #light.fade_rgb(0, 0, 0, self.step, self.delay)
            
            self.lights[lower_bound].fade_rgb(0, 0, 0, self.step, self.delay)
            self.lights[upper_bound].fade_rgb(0, 0, 0, self.step, self.delay)
            
        sleep(0.05)
    
    
    def run(self):
        
        self.enable()
        
        while self.running:
            
            # Part I: Select origin
            origin = self.selectOrigin()
            
            # Part II: Spread the light
            
            colors = self.fnord_helper.getRandomColor()
            
            for i in range(self.LIGHT_DIVERSITY):
                self.spreadLight(origin, colors, i)
                
            # Part III: Wait
            
            #self.wait()
            sleep(0.5)
            
            
    def wait(self):
        
        duration = (self.step + self.delay) * self.wait_factor
        #sleep(duration)
        sleep(0.5)
    
    
    def setSpeed(self, speed):
        
        self.speed = speed
        