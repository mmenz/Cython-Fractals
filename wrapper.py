
import subprocess

subprocess.call(['cc', 'fractal.c'])
subprocess.call(['./a.out', 'dummy', '-100000', '-100000', '100000', '100000'])

from PIL import Image
im = Image.open('test.ppm')
im.show()
