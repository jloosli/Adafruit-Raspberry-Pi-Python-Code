#!/usr/bin/python

from Adafruit_MPL115A2 import MPL115A2

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
mpl = MPL115A2(0x60, debug=True)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode

temp, pressure = mpl.getPT()

# temp = mpl.readTemperature()
# pressure = mpl.readPressure()
# altitude = mpl.readAltitude()

print "Temperature: %.2f C" % temp
print "Pressure:    %.2f hPa" % (pressure / 100.0)
#print "Altitude:    %.2f" % altitude
