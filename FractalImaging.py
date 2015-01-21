##
## FractalImaging.py
## Apply fractal to image
## Michael Menz
##

from numpy import array, sin, cos, zeros, absolute, amax, isnan, pi
from scipy.misc import imread, imsave
from PIL import Image

im_path = '/Users/menz/Desktop/Screenshots/waldos.png'

image_array = imread(im_path, 1)

real = sin(image_array/255 * pi - pi/2)
imag = cos(image_array/255 * pi)

complex_array = real + imag*complex(0,1)
expand_array = zeros(complex_array.shape)

for x in range(100):
    complex_array = complex_array**2 + complex(0, 0.1)
    ask_array = isnan(complex_array)
    expand_array += ask_array
    
   
im = Image.fromarray(expand_array)
im.save('test.gif')