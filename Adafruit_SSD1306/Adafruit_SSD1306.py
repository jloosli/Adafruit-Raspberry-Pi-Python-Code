'''*********************************************************************
This is a library for our Monochrome OLEDs based on SSD1306 drivers

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/category/63_98

These displays use SPI to communicate, 4 or 5 pins are required to  
interface

Adafruit invests time and resources providing this open source code, 
please support Adafruit and open-source hardware by purchasing 
products from Adafruit!

Written by Limor Fried/Ladyada  for Adafruit Industries.  
BSD license, check license.txt for more information
All text above, and the splash screen must be included in any redistribution
*********************************************************************'''
BLACK = 0
WHITE = 1

SSD1306_I2C_ADDRESS =  0x3C	#// 011110+SA0+RW - 0x3C or 0x3D
# Address for 128x32 is 0x3C
# Address for 128x32 is 0x3D (default) or 0x3C (if SA0 is grounded)

'''=========================================================================
    SSD1306 Displays
    -----------------------------------------------------------------------
    The driver is used in multiple displays (128x64, 128x32, etc.).
    Select the appropriate display below to create an appropriately
    sized framebuffer, etc.

    SSD1306_128_64  128x64 pixel display

    SSD1306_128_32  128x32 pixel display

    You also need to set the LCDWIDTH and LCDHEIGHT defines to an 
    appropriate size

    -----------------------------------------------------------------------*/'''
SSD1306_128_64 = false
SSD1306_128_32 = true

if SSD1306_128_64 and SSD1306_128_32:
  print "Only one SSD1306 display can be specified at once in SSD1306"
  sys.exit()
if not SSD1306_128_64 and not SSD1306_128_32:
  print "At least one SSD1306 display must be specified in SSD1306.h"
  sys.exit()

SSD1306_LCDWIDTH = 128

SSD1306_LCDHEIGHT = 64 if SSD1306_128_64 else 32

SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF

SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA

SSD1306_SETVCOMDETECT = 0xDB

SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9

SSD1306_SETMULTIPLEX = 0xA8

SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10

SSD1306_SETSTARTLINE = 0x40

SSD1306_MEMORYMODE = 0x20

SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8

SSD1306_SEGREMAP = 0xA0

SSD1306_CHARGEPUMP = 0x8D

SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

''' Scrolling  '''
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A

class Adafruit_SSD1306 : 
  
  def __init__(self, SID, SCLK, DC, RST, CS):
    continue
  Adafruit_SSD1306(int8_t RST);

  void begin(uint8_t switchvcc = SSD1306_SWITCHCAPVCC, uint8_t i2caddr = SSD1306_I2C_ADDRESS);
  void ssd1306_command(uint8_t c);
  void ssd1306_data(uint8_t c);

  void clearDisplay(void);
  void invertDisplay(uint8_t i);
  void display();

  void startscrollright(uint8_t start, uint8_t stop);
  void startscrollleft(uint8_t start, uint8_t stop);

  void startscrolldiagright(uint8_t start, uint8_t stop);
  void startscrolldiagleft(uint8_t start, uint8_t stop);
  void stopscroll(void);

  void drawPixel(int16_t x, int16_t y, uint16_t color);

 private:
  int8_t _i2caddr, sid, sclk, dc, rst, cs;
  void fastSPIwrite(uint8_t c);
  void slowSPIwrite(uint8_t c);

  volatile uint8_t *mosiport, *clkport, *csport, *dcport;
  uint8_t mosipinmask, clkpinmask, cspinmask, dcpinmask;
};