##
## video.py
## Fractal Video Maker
## Michael Menz
##

import subprocess
from PIL import Image
from numpy import arange

def makeImage(box, real, imag, iters, path, width, height):
    subprocess.call(['./a.out', 'dummy', str(box[0]), str(box[1]), str(box[2]), str(box[3]),
            str(real), str(imag), str(iters), str(width), str(height)])
    im = Image.open('test.ppm')
    im.save(path)
    
def iterVideo(box, real, imag, max_iters, path, width, height):
    for iters in range(10, max_iters+1):
        makeImage(box, real, imag, iters, "%s%05d.png"%(path, iters), width, height)
        
def imagVideo(box, real, imag_range, iters, path, width, height):
    index = 0
    for imag in imag_range:
        makeImage(box, real, imag, iters, "%s%05d.png"%(path, index), width, height)
        index += 1
        
def realVideo(box, real_range, imag, iters, path, width, height):
    index = 0
    for real in real_range:
        makeImage(box, real, imag, iters, "%s%05d.png"%(path, index), width, height)
        index += 1

        
if __name__ == '__main__':
    realVideo([-1.5,-1.5,1.5,1.5],arange(-1,1,0.01),0,50,'juliaVidExp/image', 1000, 1000)
    

