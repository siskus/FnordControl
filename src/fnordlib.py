#!/usr/bin/python
# -*- coding: utf-8-*-

from serial import Serial

class FnordBus:
    
    con = None
    
    red = 0
    green = 0
    blue = 0
    
    def __init__(self, serial_port):
        
        self.con = Serial(
            port=serial_port,
            baudrate=19200,
        )
        
        self.con.open()
    
    
    def setRGB(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b
        
        
    def getRGB(self):
        return (self.red, self.green, self.blue) 
        
        
    def update(self):
        self.fade_rgb(255, self.red, self.green, self.blue)
           
        
    def flush(self):
        self.con.flushInput()
        self.con.flushOutput()
        
        
    def sync(self, addr = 0):
        
        for x in range(15):
            self.con.write("\e")
            
        self.con.write( chr(addr) )
        
        self.flush()
        
        
    def fade_rgb(self, addr, r, g, b, step = 5, delay = 0):
        
        self.con.write( chr(addr) )
        self.con.write("\x01")
        self.con.write( chr(step) )
        self.con.write( chr(delay) )
        self.con.write( chr(r) )
        self.con.write( chr(g) )
        self.con.write( chr(b) )
        self.con.write( "\x00\x00\x00\x00\x00" )
        self.con.write( "\x00\x00\x00" )
        self.flush()
        
        
    def stop(self, addr = 255, fading = 1):
        
        self.con.write( chr(addr) )
        self.con.write("\x08")
        self.con.write( chr(fading) )
        self.con.write( "\x00\x00\x00\x00" )
        self.con.write( "\x00\x00\x00\x00\x00" )
        self.con.write( "\x00\x00\x00" )
        self.flush()

