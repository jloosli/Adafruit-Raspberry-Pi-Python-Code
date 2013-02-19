#!/usr/bin/python

import time
import datetime
from random import randrange
from Adafruit_8x8 import EightByEight
import Adafruit_LEDBackpack

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = EightByEight(address=0x70)
led = Adafruit_LEDBackpack.LEDBackpack(0x70)
led.setBrightness=1

print "Press CTRL+Z to exit"

display=0

# Continually update the 8x8 display one pixel at a time
while(True):
  for x in range(0, 8):
    for y in range(0, 8):
      grid.setPixel(x, y)
      time.sleep(0.05)
  time.sleep(0.5)
  grid.clear()
  time.sleep(0.5)

  for x in range(0,8):
    for y in range(0,8):
      grid.setPixel(randrange(8), randrange(8))
      time.sleep(0.05)
  time.sleep(0.5)
  grid.clear()
  time.sleep(0.5)
#  display += 1
#3  print "Display: %d" % display
#  led.setBrightness=display
