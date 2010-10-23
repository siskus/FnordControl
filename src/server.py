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
from fnordlib import FnordBus, FnordHelper, FnordFader
from time import sleep
import random
from threading import Thread
import sys


SERVER_PORT = 8001
IP_ADRESS = '127.0.0.1'
BUS_PORT = "/dev/ttyUSB0"
STEP = 20
DEBUG = 0

LIGHTCOUNT = 10

bus = None
lights = []
helper = None
worker = None
fader = None




class WorkerThread(Thread):
    
    lights = None
    bus = None
    fader = None
    current_fader = 0
    
    running = 0
    mode = 0
    
    speed = 0
    
    
    def __init__(self, bus, lights, fader):
        Thread.__init__(self)
        
        self.bus = bus
        self.lights = lights
        self.killed = 0
        self.speed = 0.5
        self.fader = fader
        self.current_fader = 0
        

    def fadeRandomColors(self):
                    
        for light in self.lights:
            red, green, blue = helper.getRandomColor()
            light.fade_rgb(red, green, blue, 255)
    
        for light in self.lights:
            light.fade_rgb(0, 0, 0, 10, 3)
            
        sleep( self.speed )
        
        
    def fadePureRandomColors(self):
                    
        for light in self.lights:
            
            color = int( random.random() * 3 )
            
            if color == 0:
                red, green, blue = (255, 0, 0)
            elif color == 1:
                red, green, blue = (0, 255, 0)
            elif color == 2:
                red, green, blue = (0, 0, 255)
            elif color == 3:
                red, green, blue = (0, 255, 255)
            elif color == 4:
                red, green, blue = (255, 255, 0)
            elif color == 5:
                red, green, blue = (255, 0, 255)
            elif color == 6:
                red, green, blue = (255, 255, 255)
            elif color == 7:
                red, green, blue = (0, 0, 0)
                
            light.fade_rgb(red, green, blue, 255)
    
        for light in self.lights:
            light.fade_rgb(0, 0, 0, 10, 3)
            
        sleep( self.speed )
        
        
    def setFader(self, fader):
        
        self.current_fader = fader
        
    
    def fadeCustomColors(self):
        
        for light in self.lights:
            
            red, green, blue = self.fader[self.current_fader].getColor()
            step, delay = self.fader[self.current_fader].getStepDelayJitter()
            light.fade_rgb(red, green, blue, step, delay)
            
        sleep( self.speed )
        
        
    def stroboskop(self):
        
        self.bus.fade_rgb(255, 0, 0, 0, 255)
        
        self.bus.fade_rgb(255, 255, 255, 255, 255)
        
    
    def incrSpeed(self, amount = 1.1):
        
        self.speed /= amount
        
        
    def decrSpeed(self, amount = 1.1):
        
        self.speed *= amount
       
        
    def setBPM(self, bpm):
        
        self.speed = 60.0 / bpm
        
        
    def getBPM(self):
        
        return int( 60.0 / self.speed ) 
    
    
    def run(self):
        
        if DEBUG:
            print("WorkerThread running...")
        
        while 1:
            
            while self.running:
            
                if DEBUG:
                    print("WorkerThread main loop...")        
                           
                if self.mode == 1:
                    self.fadeRandomColors()
                    
                elif self.mode == 2:
                    self.fadePureRandomColors()
                    
                elif self.mode == 3:
                    self.fadeCustomColors()
                    
                elif self.mode == 4:
                    self.stroboskop()
                    
                else:
                    self.running = 0
                    
            while not self.running:
                
                if DEBUG:
                    print("WorkerThread waiting for work...")
                sleep(1)
                    
                    
                
    def setMode(self, mode):
        
        self.mode = mode
        
        
    def stop(self):
        self.running = 0

        
    def energize(self):
        self.running = 1                    


class HappyServer(BaseHTTPRequestHandler):      
    
    def do_GET(self):

            
        action = self.path.strip("/")
        
        
        if action.startswith("fadePureColors"):
            
            worker.setMode(2)
            worker.setBPM(240)
            worker.energize()
            
     
        elif action.startswith("black"):
            
            bus.black()
           
            
        elif action.startswith("reset"):
            
            bus.reset()
            
            
        elif action.startswith("pgmColorWheel"):
            
            bus.start_program(255, 0, [5, 1, 1,  0,  0,  60, 0, 255, 255, 255] )
            
            
        elif action.startswith("pgmReverseColorWheel"):
            
            bus.start_program(255, 0, [5, 1, 1,  0,  0,  60, 0, 1, 255, 255] )
            
            
        elif action.startswith("color"):
            
            red, green, blue = map(int, action.split("/")[1:])
            bus.setRGB( red, green, blue )
            bus.update()
            
            
        elif action.startswith("fadeRandomColors"):
                    
            worker.setMode(1)
            worker.setBPM(240)
            worker.energize()
            
            
        elif action.startswith("faderCool"):
                    
            worker.setMode(3)
            worker.setFader(1)
            worker.setBPM(480)
            worker.energize()

        elif action.startswith("faderFire"):
                    
            worker.setMode(3)
            worker.setFader(0)
            worker.setBPM(480)
            worker.energize()

        
        elif action.startswith("faderWarm"):
    
            worker.setMode(3)
            worker.setFader(2)
            worker.setBPM(1024)
            worker.energize()
            
        elif action.startswith("fader2Warm"):
    
            worker.setMode(3)
            worker.setFader(4)
            worker.setBPM(480)
            worker.energize()
        
        elif action.startswith("faderIitb"):
    
            worker.setMode(3)
            worker.setFader(3)
            worker.setBPM(480)
            worker.energize()

        elif action.startswith("strobo"):
            
            worker.setMode(4)
            worker.energize()


        elif action.startswith("stop"):
            
            worker.stop()
            
            
        elif action.startswith("slower"):
            
            worker.decrSpeed()
            
            
        elif action.startswith("faster"):
            
            worker.incrSpeed()
            
        elif action.startswith("bpm"):
            
            worker.setBPM( int(action.split("/")[1]) )   
            
        elif action.startswith("apple-touch-icon.png"):
            
            self.serveFile("apple-touch-icon.png")
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( self.generateHTMLUI() )
        
        
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

      
    
    def generateHTMLUI(self):
        
        #if body == None:
        
        body = "<HTML><HEAD>"
        body += "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">"
        body += "<TITLE>FnordHappyServer V0.1 Speed: %s</TITLE></HEAD><BODY>" % worker.getBPM()
        body += """<div style="float:left"><font size="+20">"""
        body += """<a href="/fadePureColors">FadePureColors</a>"""
        body += "<br />"
        body += """<a href="/fadeRandomColors">FadeRandomColors</a>"""
        body += "<br />"
        body += """<a href="/faderCool">Fader Cool Fire</a>"""
        body += "<br />"
        body += """<a href="/faderFire">Fader Fire</a>"""
        body += "<br />"
        body += """<a href="/faderWarm">Fader Warm</a>"""
        body += "<br />"
        body += """<a href="/fader2Warm">Fader Warm Low</a>"""
        body += "<br />"
        body += """<a href="/black">Black</a>"""
        body += "<br />"
        body += """<a href="/strobo">Stroboskop</a>"""
        body += "<br />"
        body += """<a href="/faster">Faster</a>"""
        body += "<br />"
        body += """<a href="/slower">Slower</a>"""
        body += "<br />"
        body += """<a href="/pgmColorWheel">Color Wheel</a>"""
        body += "<br />"
        body += """<a href="/pgmReverseColorWheel">Reverse Color Wheel</a>"""
        body += "<br />"
        body += """<a href="/faderIitb">IITB Fader</a>"""
        body += "<br />"
        body += """<a href="/stop">Stop</a>"""
        body += ""
        body += ""
        body += "</font></div>"
        body += """<div style="float:right"><font size="+20">Colors <br />"""
        body += """<a href="/color/255/0/0">Red</a>"""
        body += "<br />"
        body += """<a href="/color/0/255/0">Green</a>"""
        body += "<br />"
        body += """<a href="/color/0/0/255">Blue</a>"""
        body += "<br />"
        body += """<a href="/color/192/255/160">Light Green</a>"""
        body += "<br />"
        body += """<a href="/color/180/60/20">Warm Red</a>"""
        body += "<br />"
        body += """<a href="/color/255/135/95">Warm Red Bright</a>"""
        body += "<br />"
        body += """<a href="/color/160/10/255">Red Blue</a>"""
        body += "<br />"
        body += """<a href="/color/255/112/0">Orange</a>"""
        body += "<br />"
        body += """<a href="/color/255/112/255">Light Blue</a>"""
        body += "<br />"
        body += """<a href="/color/255/255/255">White</a>"""
        body += "<br />"
        body += """<a href="/color/255/255/150">IITB Full</a>"""
        body += "<br />"
        body += """<a href="/color/127/127/75">IITB Half</a>"""
        body += "<br />"
        body += """<a href="/color/64/64/32">IITB Quarter</a>"""
        body += "<br />"
        body += """<a href="/reset">Reset</a>"""
        body += ""
        body += ""
        body += "</font></div>"
        body += "</BODY></HTML>"
            
        return body


class DemoServer(BaseHTTPRequestHandler):      
    
    def do_GET(self):
        
        try:
            
            action = self.path.strip("/")
    
            red, green, blue = bus.getRGB()
            
            if action.startswith("set"):
                red, green, blue = map(int, action.split("/")[1:])        
    
            elif action == "black":
                red = 0
                green = 0
                blue = 0
    
            elif action == "white":
                red = 255
                green = 255
                blue = 255
    
            elif action == "red":
                red += STEP
                if red > 255:
                    red = 255
    
            elif action == "green":
                green += STEP
                if green > 255:
                    green = 255
    
            elif action == "blue":
                blue += STEP
                if blue > 255:
                    blue = 255
            
            elif action == "nored":
                red -= STEP
                if red < 0:
                    red = 0
    
            elif action == "nogreen":
                green -= STEP
                if green < 0:
                    green = 0
    
            elif action == "noblue":
                blue -= STEP
                if blue < 0:
                    blue = 0
    
            bus.setRGB(red, green, blue)
    
            bus.update()


        except:
            pass


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( self.generateHTMLUI() )
      
    
    def generateHTMLUI(self):
        
        #if body == None:
        
        body = "<HTML><HEAD>"
        body += "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">"
        body += "<TITLE>FnordServer V0.1 (%s,%s,%s)</TITLE></HEAD><BODY>" % bus.getRGB()
    
        body += """<font size="+20">"""
        body += "<br />"
        body += """<a href="/nored">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Rot <a href="/red">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/nored">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Rot <a href="/red">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/nored">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Rot <a href="/red">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br /><br />"
        body += """<a href="/nogreen">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Gr&uuml;n <a href="/green">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/nogreen">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Gr&uuml;n <a href="/green">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/nogreen">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Gr&uuml;n <a href="/green">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br /><br />"
        body += """<a href="/noblue">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Blau <a href="/blue">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/noblue">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Blau <a href="/blue">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br />"
        body += """<a href="/noblue">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</a> Blau <a href="/blue">&gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;</a>"""
        body += "<br /><br />"
        body += """<a href="/black">Fadeout</a>"""
        body += "<br /><br />"
        body += """<a href="/white">Wei&szlig;</a>"""
        body += "<br />"
        body += "</font>"
        body += ""
        body += ""
        
        body += "</BODY></HTML>"
            
        return body

# public static void main ;-)    

if len(sys.argv) < 2:
    print("Usage: %s <server>" % sys.argv[0])
    sys.exit(-1)
    
server_type = sys.argv[1]

bus = FnordBus(BUS_PORT, False)
helper = FnordHelper()

fader = []

fire_fader = FnordFader()
fire_fader.addColor( (0, 0, 80) )
fire_fader.addColor( (255, 80, 0) )
fire_fader.setDelay(0)
fire_fader.setStep(10)

cool_fader = FnordFader()
cool_fader.addColor( (0, 255, 160) )
cool_fader.addColor( (0, 135, 0) )
cool_fader.setDelay(1)
cool_fader.setStep(1)

warm_fader = FnordFader()
warm_fader.addColor( (100, 20, 0) )
warm_fader.addColor( (180, 60, 20) )

warm2_fader = FnordFader()
warm2_fader.addColor( (100, 20, 0) )
warm2_fader.addColor( (60, 20, 0) )
warm2_fader.addColor( (20, 0, 0) )
warm2_fader.setDelay(1)
warm2_fader.setStep(1)


iitb_fader = FnordFader()
iitb_fader.addColor( (127, 127, 75) )
iitb_fader.addColor( (64, 64, 32) )
iitb_fader.setDelay(1)
iitb_fader.setStep(1)

fader.append(fire_fader)
fader.append(cool_fader)
fader.append(warm_fader)
fader.append(iitb_fader)
fader.append(warm2_fader)


for x in range(LIGHTCOUNT):
    lights.append(bus.getFnordLight(x))

worker = WorkerThread(bus, lights, fader)
worker.daemon = 1
worker.start()

try:
    
    print 'Starting FnordServer at %s:%s...' % (IP_ADRESS, SERVER_PORT)
    
    if server_type == "demo":
        server = HTTPServer((IP_ADRESS, SERVER_PORT), DemoServer)
    elif server_type == "happy":
        server = HTTPServer((IP_ADRESS, SERVER_PORT), HappyServer)
        
    server.serve_forever()
    
    
except KeyboardInterrupt:
    
    print 'Shutting down server...\n'
    worker.stop()
    sleep(1)
    server.socket.close()
    #bus.black()
    
    
