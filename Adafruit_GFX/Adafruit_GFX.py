'''******************************************************************
 This is the core graphics library for all our displays, providing
 basic graphics primitives (points, lines, circles, etc.). It needs
 to be paired with a hardware-specific library for each display
 device we carry (handling the lower-level functions).
 
 Adafruit invests time and resources providing this open
 source code, please support Adafruit and open-source hardware
 by purchasing products from Adafruit!
 
 Written by Limor Fried/Ladyada for Adafruit Industries.
 BSD license, check license.txt for more information.
 All text above must be included in any redistribution.
 ******************************************************************'''

#include "Adafruit_GFX.h"
#include "glcdfont.c"
#include <avr/pgmspace.h>

class Adafruit_GFX:
  _width = 0
  _height = 0

  def __init__(self, width, height):
    self._width = width
    self._height = height

    rotation = 0    
    cursor_y = cursor_x = 0
    textsize = 1
    textcolor = textbgcolor = 0xFFFF
    wrap = true

  ''' draw a circle outline '''
  def drawCircle(self, x0, y0, r, color):
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r

    self.drawPixel(x0, y0+r, color)
    self.drawPixel(x0, y0-r, color)
    self.drawPixel(x0+r, y0, color)
    self.drawPixel(x0-r, y0, color)

    while (x<y) {
      if (f >= 0) {
        y--
        ddF_y += 2
        f += ddF_y
      }
      x++
      ddF_x += 2
      f += ddF_x
    
      self.drawPixel(x0 + x, y0 + y, color)
      self.drawPixel(x0 - x, y0 + y, color)
      self.drawPixel(x0 + x, y0 - y, color)
      self.drawPixel(x0 - x, y0 - y, color)
      self.drawPixel(x0 + y, y0 + x, color)
      self.drawPixel(x0 - y, y0 + x, color)
      self.drawPixel(x0 + y, y0 - x, color)
      self.drawPixel(x0 - y, y0 - x, color)

  def drawCircleHelper(self,  x0, y0, r, cornername, ucolor):
    f     = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x     = 0
    y     = r

    while (x<y):
      if (f >= 0):
        y--
        ddF_y += 2
        f     += ddF_y
      
      x+=1
      ddF_x += 2
      f     += ddF_x
      if (cornername & 0x4):
        self.drawPixel(x0 + x, y0 + y, color)
        self.drawPixel(x0 + y, y0 + x, color)
       
      if (cornername & 0x2) :
        self.drawPixel(x0 + x, y0 - y, color)
        self.drawPixel(x0 + y, y0 - x, color)
      
      if (cornername & 0x8) :
        self.drawPixel(x0 - y, y0 + x, color)
        self.drawPixel(x0 - x, y0 + y, color)
      
      if (cornername & 0x1) :
        self.drawPixel(x0 - y, y0 - x, color)
        self.drawPixel(x0 - x, y0 - y, color)
      
  def fillCircle(self, x0, y0, r, ucolor):
    drawFastVLine(x0, y0-r, 2*r+1, color)
    fillCircleHelper(x0, y0, r, 3, 0, color)


''' used to do circles and roundrects!'''
  def fillCircleHelper(self, x0, y0, r, cornername, delta, ucolor):

    f     = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x     = 0
    y     = r

    while (x<y) :
      if (f >= 0) :
        y -= 1
        ddF_y += 2
        f     += ddF_y

      x += 1
      ddF_x += 2
      f     += ddF_x

      if (cornername & 0x1) :
        self.drawFastVLine(x0+x, y0-y, 2*y+1+delta, color)
        self.drawFastVLine(x0+y, y0-x, 2*x+1+delta, color)

      if (cornername & 0x2) :
        self.drawFastVLine(x0-x, y0-y, 2*y+1+delta, color)
        self.drawFastVLine(x0-y, y0-x, 2*x+1+delta, color)

''' bresenham's algorithm - thx wikpedia'''
  def drawLine(self, x0, y0, x1, y1, ucolor):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if (steep) :
      swap(x0, y0)
      swap(x1, y1)

    if (x0 > x1) :
      swap(x0, x1)
      swap(y0, y1)

    dx, dy
    dx = x1 - x0
    dy = abs(y1 - y0)

    err = dx / 2
    ystep = 0

    if (y0 < y1) :
      ystep = 1
    else:
      ystep = -1

    for ( x0<=x1 x0++) :
      if (steep) :
        self.drawPixel(y0, x0, color)
      else
        self.drawPixel(x0, y0, color)
      
      err -= dy
      if (err < 0) :
        y0 += ystep
        err += dx

''' draw a rectangle'''
  def drawRect(self, x, y, w, h, ucolor):
    self.drawFastHLine(x, y, w, color)
    self.drawFastHLine(x, y+h-1, w, color)
    self.drawFastVLine(x, y, h, color)
    self.drawFastVLine(x+w-1, y, h, color)


  def drawFastVLine(self, x, y, h, ucolor) :
  ''' stupidest version - update in subclasses if desired!'''
    self.drawLine(x, y, x, y+h-1, color)


  def drawFastHLine(self, x, y, w, ucolor) :
  ''' stupidest version - update in subclasses if desired!'''
    self.drawLine(x, y, x+w-1, y, color)

  def fillRect(self, x, y, w, h, ucolor) :
  ''' stupidest version - update in subclasses if desired!'''
    for (i=x i<x+w i++) :
      self.drawFastVLine(i, y, h, color) 


  def fillScreen(self, ucolor) :
    fillRect(0, 0, _width, _height, color)

''' draw a rounded rectangle!'''
  def drawRoundRect(self, x, y, w, h, r, ucolor) :
  ''' smarter version'''
    self.drawFastHLine(x+r  , y    , w-2*r, color) ''' Top'''
    self.drawFastHLine(x+r  , y+h-1, w-2*r, color) ''' Bottom'''
    self.drawFastVLine(  x    , y+r  , h-2*r, color) ''' Left'''
    self.drawFastVLine(  x+w-1, y+r  , h-2*r, color) ''' Right'''
    ''' draw four corners'''
    self.drawCircleHelper(x+r    , y+r    , r, 1, color)
    self.drawCircleHelper(x+w-r-1, y+r    , r, 2, color)
    self.drawCircleHelper(x+w-r-1, y+h-r-1, r, 4, color)
    self.drawCircleHelper(x+r    , y+h-r-1, r, 8, color)


''' fill a rounded rectangle!'''
  def fillRoundRect(self, x, y, w, h, r, ucolor):
  ''' smarter version'''
    draw.fillRect(x+r, y, w-2*r, h, color)

    ''' draw four corners'''
    draw.fillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, color)
    fillCircleHelper(x+r    , y+r, r, 2, h-2*r-1, color)

''' draw a triangle!'''
  def drawTriangle(self, x0, y0, x1, y1, x2, y2, ucolor):
    self.drawLine(x0, y0, x1, y1, color)
    self.drawLine(x1, y1, x2, y2, color)
    self.drawLine(x2, y2, x0, y0, color)

''' fill a triangle!'''
  def fillTriangle (self,  x0, y0, x1, y1, x2, y2, ucolor):

    a, b, y, last

    ''' Sort coordinates by Y order (y2 >= y1 >= y0)'''
    if (y0 > y1) :
      swap(y0, y1) swap(x0, x1)
    
    if (y1 > y2) :
      swap(y2, y1) swap(x2, x1)
    
    if (y0 > y1) :
      swap(y0, y1) swap(x0, x1)
    

    if(y0 == y2) : ''' Handle awkward all-on-same-line case as its own thing'''
      a = b = x0
      if(x1 < a)      a = x1
      else if(x1 > b) b = x1
      if(x2 < a)      a = x2
      else if(x2 > b) b = x2
      self.drawFastHLine(a, y0, b-a+1, color)
      return
    

    dx01 = x1 - x0,
    dy01 = y1 - y0,
    dx02 = x2 - x0,
    dy02 = y2 - y0,
    dx12 = x2 - x1,
    dy12 = y2 - y1,
    sa   = 0,
    sb   = 0

    ''' For upper part of triangle, find scanline crossings for segments'''
    ''' 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1'''
    ''' is included here (and second loop will be skipped, avoiding a /0'''
    ''' error there), otherwise scanline y1 is skipped here and handled'''
    ''' in the second loop...which also avoids a /0 error here if y0=y1'''
    ''' (flat-topped triangle).'''
    if(y1 == y2) last = y1   ''' Include y1 scanline'''
    else         last = y1-1 ''' Skip it'''

    for(y=y0 y<=last y++) :
      a   = x0 + sa / dy01
      b   = x0 + sb / dy02
      sa += dx01
      sb += dx02
      ''' longhand:
      a = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
      b = x0 + (x2 - x0) * (y - y0) / (y2 - y0)
      '''
      if(a > b): swap(a,b)
      self.drawFastHLine(a, y, b-a+1, color)
    

    ''' For lower part of triangle, find scanline crossings for segments'''
    ''' 0-2 and 1-2.  This loop is skipped if y1=y2.'''
    sa = dx12 * (y - y1)
    sb = dx02 * (y - y0)
    for( y<=y2 y++) :
      a   = x1 + sa / dy12
      b   = x0 + sb / dy02
      sa += dx12
      sb += dx02
      ''' longhand:
      a = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
      b = x0 + (x2 - x0) * (y - y0) / (y2 - y0)
      '''
      if(a > b) swap(a,b)
      self.drawFastHLine(a, y, b-a+1, color)

  def drawBitmap(self, x, y, const *bitmap, w, h, ucolor) :

    i, j, byteWidth = (w + 7) / 8

    for(j=0 j<h j++) :
      for(i=0 i<w i++ ) :
        if(pgm_read_byte(bitmap + j * byteWidth + i / 8) & (128 >> (i & 7))) :
  	self.drawPixel(x+i, y+j, color)


  def write(self, c) :
    if (c == '\n') :
      cursor_y += textsize*8
      cursor_x = 0
    elif (c == '\r') :
      ''' skip em'''
    else:
      self.drawChar(cursor_x, cursor_y, c, textcolor, textbgcolor, textsize)
      cursor_x += textsize*6
      if (wrap && (cursor_x > (_width - textsize*6))) {
        cursor_y += textsize*8
        cursor_x = 0
    return 1

''' draw a character'''
  def drawChar(self, x, y, unsigned char c, ucolor, ubg, size) :

    if((x >= _width)            || ''' Clip right'''
       (y >= _height)           || ''' Clip bottom'''
       ((x + 5 * size - 1) < 0) || ''' Clip left'''
       ((y + 8 * size - 1) < 0))   ''' Clip top'''
      return

    for (i=0; i<6; i++ ) {
      line = 0
      if (i == 5) :
        line = 0x0
      else: 
        line = pgm_read_byte(font+(c*5)+i)
      for (int8_t j = 0 j<8 j++) :
        if (line & 0x1) :
          if (size == 1): ''' default size'''
            self.drawPixel(x+i, y+j, color)
          else :  ''' big size'''
            fillRect(x+(i*size), y+(j*size), size, size, color)

        else if (bg != color) :
          if (size == 1): ''' default size'''
            self.drawPixel(x+i, y+j, bg)
          else :  ''' big size'''
            fillRect(x+i*size, y+j*size, size, size, bg)
        line >>= 1

  def setCursor(self, x, y) :
    cursor_x = x
    cursor_y = y



  def setTextSize(self, s) :
    textsize = (s > 0) ? s : 1



  def setTextColor(self, uc) :
    textcolor = c
    textbgcolor = c 
    ''' for 'transparent' background, we'll set the bg '''
    ''' to the same as fg instead of using a flag'''


   def setTextColor(self, uc, ub) :
     textcolor = c
     textbgcolor = b 
 

  def setTextWrap(self, w) :
    wrap = w

  def getRotation(self, ) :
    rotation %= 4
    return rotation


  def setRotation(self, x) :
    x %= 4  ''' cant be higher than 3'''
    rotation = x
    switch (x) {
    case 0:
    case 2:
      _width = WIDTH
      _height = HEIGHT
      break
    case 1:
    case 3:
      _width = HEIGHT
      _height = WIDTH
      break

  def invertDisplay(self, i) :
  ''' do nothing, can be subclassed'''
    continue


  ''' return the size of the display which depends on the rotation!'''
  def width(self) :
    return _width 
  
 
  def height(self): 
    return _height 
