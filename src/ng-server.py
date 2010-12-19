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
#IP_ADRESS = '192.168.3.100'
IP_ADRESS = '127.0.0.1'
BUS_PORT = "/dev/ttyUSB0"
STEP = 20
DEBUG = 1

LIGHTCOUNT = 10

bus = None
worker = None
helper = None

class  WorkerThread(Thread):
    
    def __init__(self, bus):
        Thread.__init__(self)
        
        self.running = 0
        self.bus = bus
        self.command = 0
        
        self.fader = None
        
    
    def execute(self, command):
        self.command = command
        
        
    def go(self):
        self.running = 1
        
        
    def halt(self):
        self.running = 0
        
        
    def run(self):
        pass


class FnordServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        action = self.path.strip("/")
        
        if DEBUG:
            print("Path: %s" % action)
        
        commands = action.split("/")
        
        
        if commands[0] == "default.css":
            self.serveFile("default.css")
            
        elif commands[0] == "apple-touch-icon.png":
            self.serveFile("apple-touch-icon.png")
            
        else:
            self.sendHTMLUI()


    def sendHTMLUI(self):
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
        
        
    def generateHTMLUI(self, title = "Fnord-Control NG", command = "",
                       speed = "", message = ""):
        
        body = ""
        
        filename = "index.html"
        
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

#bus = FnordBus(BUS_PORT, False)
helper = FnordHelper()
worker = WorkerThread(bus)
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
        