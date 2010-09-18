#!/usr/bin/env python
# -*- coding: utf-8-*-

#         fnordlib demo controller
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


from fnordlib import FnordBus
from time import sleep


PORT = "/dev/ttyUSB0"


# public static void main ;-)

bus = FnordBus(PORT)

bus.sync()
bus.stop()

#bus.fade_rgb2(255, 255, 255, 255)

print("Program running...")

try:
    for x in range(1000):
        
        value = (x * 20) % 256
        bus.fade_rgb(255, value, value, value)
        
        sleep(1)
        
except KeyboardInterrupt:
    print("Shutting down...\n")
    bus.black()