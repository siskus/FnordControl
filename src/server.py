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

from fnordlib import FnordBus

SERVER_PORT = 8000
IP_ADRESS = '127.0.0.1'
BUS_PORT = "/dev/ttyUSB0"
STEP = 20
DEBUG = 1

bus = None


class ServerHandler(BaseHTTPRequestHandler):      
    
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

bus = FnordBus(BUS_PORT)


try:
    
    print 'Starting FnordServer at %s:%s...' % (IP_ADRESS, SERVER_PORT)
    
    server = HTTPServer((IP_ADRESS, SERVER_PORT), ServerHandler)
    server.serve_forever()
    
    
except KeyboardInterrupt:
    
    print 'Shutting down server...\n'
    server.socket.close()
    bus.black()
    
    