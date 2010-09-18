#!/usr/bin/python
# -*- coding: utf-8-*-

from fnordlib import FnordBus
from time import sleep


PORT = "/dev/ttyUSB0"


# public static void main ;-)

bus = FnordBus(PORT)

bus.sync()
bus.stop()

for x in range(1000):
    
    value = (x * 20) % 256
    bus.fade_rgb(255, value, value, value)
    
    sleep(1)