#!/usr/bin/python

import time
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# MPL115A2 Class
# ===========================================================================

class MPL115A2 :
  i2c = None

  # Operating Modes
  __BMP085_ULTRALOWPOWER     = 0
  __BMP085_STANDARD          = 1
  __BMP085_HIGHRES           = 2
  __BMP085_ULTRAHIGHRES      = 3

  # BMP085 Registers
  __BMP085_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
  __BMP085_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)
  __BMP085_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)
  __BMP085_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)
  __BMP085_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
  __BMP085_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
  __BMP085_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
  __BMP085_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
  __BMP085_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
  __BMP085_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
  __BMP085_CAL_MD            = 0xBE  # R   Calibration data (16 bits)
  __BMP085_CONTROL           = 0xF4
  __BMP085_TEMPDATA          = 0xF6
  __BMP085_PRESSUREDATA      = 0xF6
  __BMP085_READTEMPCMD       = 0x2E
  __BMP085_READPRESSURECMD   = 0x34

  # Private Fields
  _cal_AC1 = 0
  _cal_AC2 = 0
  _cal_AC3 = 0
  _cal_AC4 = 0
  _cal_AC5 = 0
  _cal_AC6 = 0
  _cal_B1 = 0
  _cal_B2 = 0
  _cal_MB = 0
  _cal_MC = 0
  _cal_MD = 0

  """=========================================================================
    REGISTERS
    -----------------------------------------------------------------------"""
  __MPL115A2_REGISTER_PRESSURE_MSB =        0x00
  __MPL115A2_REGISTER_PRESSURE_LSB =        0x01
  __MPL115A2_REGISTER_TEMP_MSB      =       0x02
  __MPL115A2_REGISTER_TEMP_LSB      =       0x03
  __MPL115A2_REGISTER_A0_COEFF_MSB   =      0x04
  __MPL115A2_REGISTER_A0_COEFF_LSB    =     0x05
  __MPL115A2_REGISTER_B1_COEFF_MSB    =     0x06
  __MPL115A2_REGISTER_B1_COEFF_LSB     =    0x07
  __MPL115A2_REGISTER_B2_COEFF_MSB     =    0x08
  __MPL115A2_REGISTER_B2_COEFF_LSB      =   0x09
  __MPL115A2_REGISTER_C12_COEFF_MSB     =   0x0A
  __MPL115A2_REGISTER_C12_COEFF_LSB     =   0x0B
  __MPL115A2_REGISTER_STARTCONVERSION   =   0x12

  '''========================================================================='''

  """=========================================================================
    PRIVATE FIELDS
    -----------------------------------------------------------------------"""

  _mpl115a2_a0 = 0
  _mpl115a2_b1 = 0
  _mpl115a2_b2 = 0
  _mpl115a2_c12 = 0
  
  # Constructor
  def __init__(self, address=0x60, mode=1, debug=False):
    self.i2c = Adafruit_I2C(address, debug=debug)

    self.address = address
    self.debug = debug
    # Make sure the specified mode is in the appropriate range
    # if ((mode < 0) | (mode > 3)):
    #   if (self.debug):
    #     print "Invalid Mode: Using STANDARD by default"
    #   self.mode = self.__BMP085_STANDARD
    # else:
    #   self.mode = mode
    # # Read the calibration data
    self.readCalibrationData()

  def readCalibrationData(self):
    "Reads the calibration data from the IC"
    self._mpl115a2_a0 = 0
    self._mpl115a2_b1 = 0
    self._mpl115a2_b2 = 0
    self._mpl115a2_c12 = 0

    self._mpl115a2_a0 = self.i2c.readS8(self.__MPL115A2_REGISTER_A0_COEFF_MSB)   # INT16
    self._mpl115a2_a0 = self._mpl115a2_a0 << 8 | self.i2c.readU8(self.__MPL115A2_REGISTER_A0_COEFF_LSB)   # INT16
    self._mpl115a2_b1 = self.i2c.readS8(self.__MPL115A2_REGISTER_B1_COEFF_MSB)   # INT16
    self._mpl115a2_b1 = self._mpl115a2_b1 << 8 | self.i2c.readU8(self.__MPL115A2_REGISTER_B1_COEFF_LSB)   # INT16
    self._mpl115a2_b2 = self.i2c.readS8(self.__MPL115A2_REGISTER_B2_COEFF_MSB)   # INT16
    self._mpl115a2_b2 = self._mpl115a2_b2 << 8 | self.i2c.readU8(self.__MPL115A2_REGISTER_B2_COEFF_LSB)   # INT16
    self._mpl115a2_c12 = self.i2c.readS8(self.__MPL115A2_REGISTER_C12_COEFF_MSB)   # INT16
    self._mpl115a2_c12 = self._mpl115a2_c12 << 8 | self.i2c.readU8(self.__MPL115A2_REGISTER_C12_COEFF_LSB)   # INT16
    self._mpl115a2_c12 = self._mpl115a2_c12 >> 2

    print(self._mpl115a2_a0)
    self._mpl115a2_a0 /= 8.0
    print(self._mpl115a2_a0)
    self._mpl115a2_b1 /= 8192.0
    self._mpl115a2_b2 /= 16384.0
    self._mpl115a2_c12 /= 4194304.0
    #self._mpl115a2_c12 /= 10**9

    if (self.debug):
      self.showCalibrationData()

  def showCalibrationData(self):
      "Displays the calibration values for debugging purposes"
      print "DBG: A0 = %f" % (self._mpl115a2_a0)
      print(self._mpl115a2_a0)
      print "DBG: B1 = %f" % (self._mpl115a2_b1)
      print "DBG: B2 = %f" % (self._mpl115a2_b2)
      print "DBG: C12 = %.20f" % (self._mpl115a2_c12)

  def readRawTemp(self):
    "Reads the raw (uncompensated) temperature from the sensor"
    self.i2c.write8(self.__BMP085_CONTROL, self.__BMP085_READTEMPCMD)
    time.sleep(0.005)  # Wait 5ms
    raw = self.i2c.readU16(self.__BMP085_TEMPDATA)
    if (self.debug):
      print "DBG: Raw Temp: 0x%04X (%d)" % (raw & 0xFFFF, raw)
    return raw

  def getPT(self):
    "Read Temperature and Pressure"
    self.i2c.write8(0xC0,0x00)
    self.i2c.write8(self.__MPL115A2_REGISTER_STARTCONVERSION, 0x00)
    time.sleep(0.005) # Wait 5ms
    self.i2c.write8(0xC1,0x00)
    #self.i2c.write8(self.__MPL115A2_REGISTER_PRESSURE_MSB, 0x00)
    pressure = ((self.i2c.readU8(self.__MPL115A2_REGISTER_PRESSURE_MSB) << 8) | self.i2c.readU8(self.__MPL115A2_REGISTER_PRESSURE_LSB)) >> 6
    temp = ((self.i2c.readU8(self.__MPL115A2_REGISTER_TEMP_MSB) << 8) | self.i2c.readU8(self.__MPL115A2_REGISTER_TEMP_LSB)) >> 6

    pressureComp = self._mpl115a2_a0 + (self._mpl115a2_b1 + self._mpl115a2_c12 * temp) * pressure + self._mpl115a2_b2 * temp
    P = ((65.0 / 1023) * pressureComp) + 50.0
    T = ((temp - 498.0) / -5.35 + 25.0)
    return P,T, temp


  def readRawPressure(self):
    "Reads the raw (uncompensated) pressure level from the sensor"
    self.i2c.write8(self.__BMP085_CONTROL, self.__BMP085_READPRESSURECMD + (self.mode << 6))
    if (self.mode == self.__BMP085_ULTRALOWPOWER):
      time.sleep(0.005)
    elif (self.mode == self.__BMP085_HIGHRES):
      time.sleep(0.014)
    elif (self.mode == self.__BMP085_ULTRAHIGHRES):
      time.sleep(0.026)
    else:
      time.sleep(0.008)
    msb = self.i2c.readU8(self.__BMP085_PRESSUREDATA)
    lsb = self.i2c.readU8(self.__BMP085_PRESSUREDATA+1)
    xlsb = self.i2c.readU8(self.__BMP085_PRESSUREDATA+2)
    raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.mode)
    if (self.debug):
      print "DBG: Raw Pressure: 0x%04X (%d)" % (raw & 0xFFFF, raw)
    return raw

  def readTemperature(self):
    "Gets the compensated temperature in degrees celcius"
    UT = 0
    X1 = 0
    X2 = 0
    B5 = 0
    temp = 0.0

    # Read raw temp before aligning it with the calibration values
    UT = self.readRawTemp()
    X1 = ((UT - self._cal_AC6) * self._cal_AC5) >> 15
    X2 = (self._cal_MC << 11) / (X1 + self._cal_MD)
    B5 = X1 + X2
    temp = ((B5 + 8) >> 4) / 10.0
    if (self.debug):
      print "DBG: Calibrated temperature = %f C" % temp
    return temp

  def readPressure(self):
    "Gets the compensated pressure in pascal"
    UT = 0
    UP = 0
    B3 = 0
    B5 = 0
    B6 = 0
    X1 = 0
    X2 = 0
    X3 = 0
    p = 0
    B4 = 0
    B7 = 0

    UT = self.readRawTemp()
    UP = self.readRawPressure()

    # You can use the datasheet values to test the conversion results
    # dsValues = True
    dsValues = False

    if (dsValues):
      UT = 27898
      UP = 23843
      self._cal_AC6 = 23153
      self._cal_AC5 = 32757
      self._cal_MC = -8711
      self._cal_MD = 2868
      self._cal_B1 = 6190
      self._cal_B2 = 4
      self._cal_AC3 = -14383
      self._cal_AC2 = -72
      self._cal_AC1 = 408
      self._cal_AC4 = 32741
      self.mode = self.__BMP085_ULTRALOWPOWER
      if (self.debug):
        self.showCalibrationData()

    # True Temperature Calculations
    X1 = ((UT - self._cal_AC6) * self._cal_AC5) >> 15
    X2 = (self._cal_MC << 11) / (X1 + self._cal_MD)
    B5 = X1 + X2
    if (self.debug):
      print "DBG: X1 = %d" % (X1)
      print "DBG: X2 = %d" % (X2)
      print "DBG: B5 = %d" % (B5)
      print "DBG: True Temperature = %.2f C" % (((B5 + 8) >> 4) / 10.0)

    # Pressure Calculations
    B6 = B5 - 4000
    X1 = (self._cal_B2 * (B6 * B6) >> 12) >> 11
    X2 = (self._cal_AC2 * B6) >> 11
    X3 = X1 + X2
    B3 = (((self._cal_AC1 * 4 + X3) << self.mode) + 2) / 4
    if (self.debug):
      print "DBG: B6 = %d" % (B6)
      print "DBG: X1 = %d" % (X1)
      print "DBG: X2 = %d" % (X2)
      print "DBG: B3 = %d" % (B3)

    X1 = (self._cal_AC3 * B6) >> 13
    X2 = (self._cal_B1 * ((B6 * B6) >> 12)) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (self._cal_AC4 * (X3 + 32768)) >> 15
    B7 = (UP - B3) * (50000 >> self.mode)
    if (self.debug):
      print "DBG: X1 = %d" % (X1)
      print "DBG: X2 = %d" % (X2)
      print "DBG: B4 = %d" % (B4)
      print "DBG: B7 = %d" % (B7)

    if (B7 < 0x80000000):
      p = (B7 * 2) / B4
    else:
      p = (B7 / B4) * 2

    X1 = (p >> 8) * (p >> 8)
    X1 = (X1 * 3038) >> 16
    X2 = (-7375 * p) >> 16
    if (self.debug):
      print "DBG: p  = %d" % (p)
      print "DBG: X1 = %d" % (X1)
      print "DBG: X2 = %d" % (X2)

    p = p + ((X1 + X2 + 3791) >> 4)
    if (self.debug):
      print "DBG: Pressure = %d Pa" % (p)

    return p

  def readAltitude(self, seaLevelPressure=101325):
    "Calculates the altitude in meters"
    altitude = 0.0
    pressure = float(self.readPressure())
    altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
    if (self.debug):
      print "DBG: Altitude = %d" % (altitude)
    return altitude

    return 0
