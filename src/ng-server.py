#!/usr/bin/env python
# -*- coding: utf-8-*-

#         fnordlight server
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

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from FnordLib import FnordBus, FnordHelper, FnordCluster
from FnordController.fader import FnordFaderArray
from FnordController.fireworks import FireWorks
from FnordController.xmas import XMas
from FnordController.raindrops import Raindrops
from FnordLib import FnordBusDummy
from time import sleep
import random
from threading import Thread
import sys

SERVER_PORT = 8001
IP_ADRESS = '192.168.3.102'
#IP_ADRESS = '192.168.1.195'
#IP_ADRESS = '127.0.0.1'
#BUS_PORT = "/dev/ttyUSB1"
DEBUG = 1

#LIGHTCOUNT = 10

worker = None
helper = None
lightchain = []

class  WorkerThread(Thread):
    
#    running = 0
#    bus = None
#    command = None
    
    def __init__(self):
        Thread.__init__(self)
        
        self.running = 0
        self.command = None
        
    
    def setPayload(self, command):
        
        if not self.command == None:
            self.command.disable()
            self.halt()
            
        self.command = command
        
        
    def go(self):
        self.running = 1
        self.command.enable()
        
        
    def halt(self):
        self.running = 0
        self.command.disable()
        
        
    def run(self):
        
        # Loop forever
        while 42:
            
            while self.running:
                
                if self.command == None:
                    sleep(0.5)
                else:        
                    self.command.run()
                
            sleep(0.5)

            
    def setSpeed(self, speed):
        
        if not self.command == None:
            self.command.setSpeed(speed)


class FnordServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        action = self.path.strip("/")
        
        if DEBUG:
            print("Path: %s" % action)
        
        commands = action.split("/")
        
        try:
        
            if commands[0] == "default.css":
                self.serveFile("Ressources/default.css")
                
            elif commands[0] == "apple-touch-icon.png":
                self.serveFile("Ressources/apple-touch-icon.png")
    
            elif commands[0] == "one_color" or commands[0] == "xcolors":
                
                lights = []
                
                if commands[0] == "xcolors":
                    
                    for i in range(len(lightchain)):
                        lights.append(lightchain[i])
                        
                else:
                    
                    cluster = FnordCluster()
                    
                    for i in range(len(lightchain)):
                        cluster.registerLight(lightchain[i])
                        
                    lights.append(cluster)
                    
                fader = FnordFaderArray(lights)
                
                # Part 1: Configure fader
                
                if commands[1] == "rainbow":
                    
                    fader.addColor( (255, 000, 000) )
                    fader.addColor( (255, 255, 000) )
                    fader.addColor( (000, 255, 000) )
                    fader.addColor( (000, 255, 255) )
                    fader.addColor( (000, 000, 255) )          
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(10)
                    
                elif commands[1] == "iitb":
                    
                    fader.addColor( (127, 127, 075) )
                    fader.addColor( (064, 064, 032) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(1.0)
                    
                elif commands[1] == "fire":
                
                    fader.addColor( (100, 020, 000) )
                    fader.addColor( (060, 020, 000) )
                    fader.addColor( (020, 000, 000) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(2.0)
                
                elif commands[1] == "black":
                    
                    fader.addColor( (000, 000, 000) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(1.0)
                    
                elif commands[1] == "white":
                    
                    fader.addColor( (255, 255, 255) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(1.0)
                    
                elif commands[1] == "bnw":
                    
                    fader.addColor( (255, 255, 255) )
                    fader.addColor( (000, 000, 000) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(1.0)
                    
                elif commands[1] == "disco":
                    
                    fader.addColor( (255, 000, 000) )
                    fader.addColor( (255, 255, 000) )
                    fader.addColor( (000, 255, 000) )
                    fader.addColor( (000, 255, 255) )
                    fader.addColor( (000, 000, 255) )          
                    fader.setDelay(0)
                    fader.setStep(50)
                    fader.setSpeed(0.25)
                    fader.disableRandom()
                    
                else:
                    
                    fader.addColor( (000, 000, 000) )
                    fader.setDelay(0)
                    fader.setStep(1)
                    fader.setSpeed(1.0)
                    
                # Part 2: Launch thread
                worker.setPayload(fader)
                worker.go()
                
                # Part 3: Display UI
                self.sendHTMLUI("Fader changed to %s" % commands[1])
            
            elif commands[0] == "speed":
                
                try:
                    speed = int(commands[1])
                except:
                    speed = 100
                
                if speed < 25:
                    speed = 25
                elif speed > 400:
                    speed = 400
                    
                speed = 100.0 / speed
                
                # Part 1: Change speed
                worker.setSpeed(speed)
                
                # Part 2: Display UI
                self.sendHTMLUI("Speed changed to %s" % (1 / speed))
            
            elif commands[0] == "highlight":
                
                if commands[1] == "fireworks":
                    
                    controller = FireWorks(lightchain)
                    worker.setPayload(controller)
                    worker.go()
    
                elif commands[1] == "x-mas":
                    
                    controller = XMas(lightchain)
                    worker.setPayload(controller)
                    worker.go()
                    
                elif commands[1] == "raindrops":
                    
                    mode = int(commands[2])
                    
                    controller = Raindrops(lightchain, mode)
                    worker.setPayload(controller)
                    worker.go()
                
                
                self.sendHTMLUI("Switched to %s" % commands[1])
                
            else:
                
                self.sendHTMLUI()
                
                
        except IndexError:
            
            self.sendHTMLUI("Error: Invalid parameters")
                    


    def sendHTMLUI(self,  command = "", speed = "", message = "",
                   title = "Fnord-Control NG"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( self.generateHTMLUI(command, speed, message, title) )
        
        
    def serveFile(self, filename):
        
        file = open(filename, 'r')
        self.send_response(200)
        self.send_header('Content-type', self.getContentType(filename))
        self.end_headers()
        self.wfile.write(file.read())
        file.close()

        
    def getContentType(self, filename):

        type = "application/octet-stream"
    
        if filename.lower().endswith("avi"):
            type = 'video/x-msvideo'
        elif filename.lower().endswith("mkv"):
            type = 'video/x-matroska'
        elif filename.lower().endswith("mpg"):
            type = 'video/mpeg'
        elif filename.lower().endswith("iso"):
            type = 'application/x-iso9660-image'
        elif filename.lower().endswith("png"):
            type = 'image/png'
        
        return type
        
        
    def generateHTMLUI(self, command, speed, message, title):
        
        body = ""
        
        filename = "Ressources/index.html"
        
        file = open(filename, 'r')
        
        for line in file.readlines():
            body += line
            
        file.close()
        
        # Replace special values in HTML File
        body = body.replace("#TITLE#", title)
        body = body.replace("#COMMAND#", command)
        body = body.replace("#SPEED#", speed)
        body = body.replace("#MESSAGE#", message)
        
        return body
    
    
# public static void main ;-)

#bus = FnordBus(BUS_PORT)
#bus = FnordBusDummy(BUS_PORT)

# Setup for the new year

# Layout:
#
#0 1 2 3 4 ---------- 0 1 2 3 4
#=========            =========
#  Bus 1                Bus 2

bus1 = FnordBus("/dev/ttyUSB0")
bus2 = FnordBus("/dev/ttyUSB1")

for i in range(4):
    lightchain.append(bus1.getFnordLight(i))
    
cluster = FnordCluster()

cluster.registerLight(bus1.getFnordLight(4))
cluster.registerLight(bus2.getFnordLight(0))

lightchain.append(cluster)

for i in range(4):
    lightchain.append(bus2.getFnordLight(i + 1))


helper = FnordHelper()
worker = WorkerThread()

worker.daemon = 1
worker.start()

try:
    
    print 'Starting FnordServer at %s:%s...' % (IP_ADRESS, SERVER_PORT)
    
    server = HTTPServer((IP_ADRESS, SERVER_PORT), FnordServer)
    server.serve_forever()
    
    
except KeyboardInterrupt:
    
    print 'Shutting down server...\n'
    sleep(1)
    server.socket.close()    
        
