#!/usr/bin/env python
import cgi
import sys
import Image, ImageDraw
import math
from cmath import *

# Domain Coloring Ranges
height = 400
width = 400
real_min = -4.0
real_max = 4.0
imag_min = -4.0
imag_max = 4.0

# Set up for safe eval
safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh'] 
safe_dict = dict([ (k, globals().get(k, None)) for k in safe_list ]) 
safe_dict['abs'] = abs 

# fun -- user defined function
# c -- current complex value
# x -- x coordinate of the drawing
# y -- y coordinate of the drawing
def evalUserFunction( fun, c, x, y ):
   safe_dict['x'] = x
   safe_dict['y'] = y
   safe_dict['c'] = c 
   safe_dict['i'] = i 
   return eval(fun,{"__builtins__":None},safe_dict) 

# Domain coloring algorithm
def colorDomain( fun ):
   im = Image.new('RGB', (height, width))
   draw = ImageDraw.ImageDraw(im)

   i = complex(0,1)
   for jc in range(0,height):
      imag = imag_max - (imag_max - imag_min) * jc /(height-1.0)
      for ic in range(0,width):
         real = real_max - (real_max - real_min) * ic/(width - 1.0)
         c = complex(real, imag)
         x = ic
         y = jc
         v = eval(fun)
         m = sqrt( v.real**2 + v.imag**2 ) 
         a = phase(c)
         while a < 0: 
            a += 2.0*math.pi
         a /= 2.0*math.pi

         range_start = 0.0
         range_end = 1.0
         while m.real > range_end:
            range_start = range_end
            range_end *= math.e
         k = ( m.real - range_start) / ( range_end - range_start )
         sat = 0.0
         if k < .5:
            sat = k*2.0
         else:
            1 - ( k - .5 )*2.0

         val = sat
         sat = 1.0 - (1.0-sat) ** (3.0) 
         sat = .4 + sat * .6
         val = 1.0 - val;
         val = 1.0 - (1.0 - val) ** (3.0)
         val = .6 + val * .4
         r, g, b = 0, 0, 0
         if sat == 0:
            r = g = b = val
         else:
            if a == 1: 
               a = 0
            z = math.floor(a*6);
            w = int(z)
            f = a*6.0 - z
            p = val * ( 1.0 - sat)
            q = val * ( 1.0 - sat*f)
            t = val * (1.0-sat * (1.0-f))
            if w == 0:
               r = val
               g = t
               b = p
            elif w == 1:
               r = q
               g = val
               b = p
            elif w == 2:
               r = p
               g = val
               b = t
            elif w == 3:
               r = p
               g = q
               b = val
            elif w == 4:
               r = t
               g = p
               b = val
            elif w == 5:
               r = val
               g = p
               b = q 
         r *= 256
         g *= 256
         b *= 256
         if r > 255: 
            r = 255
         if g > 255: 
            g = 255
         if b > 255: 
            b = 255
         draw.point((ic,jc), fill=( int(r), int(g), int(b) ) )
   del draw
   print "Content-Type: image/png\r\n"
   im.save(sys.stdout, "PNG")

# Startup code: Parse input and call domain coloring
form = cgi.FieldStorage()
if form.has_key("fun") and form.has_key("captcha") and form["captcha"].value == "2":
   user_func=(form["fun"].value).replace("plus", "+")
   colorDomain( user_func ) 
else:
   print "Content-Type: text/html\r\n"
   print "Invalid Captcha, or bad input"
