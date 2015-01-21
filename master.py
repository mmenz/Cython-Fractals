#
# master.py
# controls fractal viewing application
# Michael Menz
#

from Tkinter import*
import subprocess
from PIL import Image, ImageTk
import tkFileDialog
from string import find

WIDTH = 750.
LENGTH = 750.

class ImageWindow(Canvas):

    def click(self, event):
        if self.zooming:
            x, y = event.x, self.y + abs(event.x - self.x)
            cbox = self.cbox
            print self.x, self.y, event.x, event.y
            self.generateAndDisplay([min(x, self.x) / WIDTH *(cbox[2] - cbox[0]) + cbox[0],
                                     min(y, self.y) / LENGTH *(cbox[3] - cbox[1]) + cbox[1],
                                     max(x, self.x) / WIDTH *(cbox[2] - cbox[0]) + cbox[0],
                                     max(y, self.y) / LENGTH *(cbox[3] - cbox[1]) + cbox[1]],
                                     self.parent.getReal(),
                                     self.parent.getImag())
            self.delete('box')
            self.zooming = False
        else:
            self.zooming = True
            self.x = event.x
            self.y = event.y

    def move(self, event):
        if self.zooming:
            self.delete('box')
            self.create_rectangle(self.x, self.y, event.x, self.y + abs(event.x - self.x), outline='white', tags='box')

    def generateAndDisplay(self, box, real, imag):
        self.cbox = box
        subprocess.call(['./a.out', 'dummy', str(box[0]), str(box[1]), str(box[2]), str(box[3]),
            str(real), str(imag), str(100), '750', '750'])
        im = Image.open('test.ppm')
        print('Image generated')
        self.image = ImageTk.PhotoImage(im)
        self.delete('all')
        self.create_image(375,375,image=self.image)

    def __init__(self, master):
        Canvas.__init__(self, master, width=750, height=750, bg= 'black', highlightthickness=0)
        self.image = None
        self.bind('<1>', self.click)
        self.bind('<Motion>', self.move)
        self.zooming = False
        self.x = 0
        self.y = 0
        self.cbox = [-2., -2., 2., 2.]
        self.parent = master

class mainFrame(Frame):

    def getReal(self):
        return self.realScale.get()

    def getImag(self):
        return self.imagScale.get()

    def Reset(self):
        self.iw.cbox = [-2.,-2., 2., 2.]
        self.scaleChanged(None)

    def Save(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if not filename:
            return
        if find(filename, '.') == -1:
            filename += '.png'
        box = self.iw.cbox
        real = self.getReal()
        imag = self.getImag()
        subprocess.call(['./a.out', 'dummy', str(box[0]), str(box[1]), str(box[2]), str(box[3]),
            str(real), str(imag), '100','4000', '4000'])
        im = Image.open('test.ppm')
        im.save(filename)

    def scaleChanged(self, event):
        self.iw.generateAndDisplay(self.iw.cbox, self.getReal(), self.getImag())

    def __init__(self, master):
        Frame.__init__(self, master, width=850, height=750, bg='black')
        self.iw = ImageWindow(self)

        ## real constant value slider and reset button
        self.realFrame = Frame(self, bg='black', width=100, height=600)
        self.realLabel = Label(self.realFrame, text="real", bg='black', fg='white')
        self.realScale = Scale(self.realFrame, from_=-1, to=1, resolution=0.001, length=600, bg='black', fg='white')
        self.realScale.bind("<ButtonRelease-1>", self.scaleChanged)
        self.realScale.set(0)
        self.resetButton = Button(self.realFrame, text='Reset', command = self.Reset)
        self.realLabel.pack(side=TOP)
        self.resetButton.pack(side=BOTTOM)
        self.realScale.pack(side=BOTTOM)

        ## imaginary constant value slider and save button
        self.imagFrame = Frame(self, bg='black', width=100, height=600)
        self.imagLabel = Label(self.imagFrame, text="imag", bg='black', fg='white')
        self.imagScale = Scale(self.imagFrame, from_=-1, to=1, resolution=0.001, length=600, bg='black', fg='white')
        self.imagScale.bind("<ButtonRelease-1>", self.scaleChanged)
        self.imagScale.set(0)
        self.saveButton = Button(self.imagFrame, text='Save', command = self.Save)
        self.imagLabel.pack(side=TOP)
        self.saveButton.pack(side=BOTTOM)
        self.imagScale.pack(side=BOTTOM)

        ## options for saving files
        self.file_opt = options = {}
        options['filetypes'] = [('png files', '.png'), ('gif files', '.gif')]
        options['initialfile'] = 'fractal.png'
        options['parent'] = root

        self.iw.pack(side=LEFT)
        self.realFrame.pack(side=RIGHT, fill=X)
        self.imagFrame.pack(side=RIGHT, fill=X)

class ColorPane(Canvas):

    def updateColorFile(self):
        f = open('color.col', 'w')
        for c in self.red + self.green + self.blue:
            f.write("%d "%(max(0, min(c, 255))))
        f.close()

    def readFromColorFile(self):
        f = open('color.col', 'r')
        text = f.read()
        strs = text.split(' ')[0:-1]
        index = 0
        for s in strs:
            if index < 256:
                self.red.append(int(s))
                if index == 0:
                    self.create_oval(17, 276-int(s)-3, 23, 276-int(s)+3, fill='red', tags='red')
                elif index == 255:
                    self.create_oval(17+3*index, 276-int(s)-3, 23+3*index, 276-int(s)+3, fill='red', tags='red')
                elif index > 0:
                    self.create_line(17+3*index, 276-self.red[-2], 20+3*index, 276-self.red[-1], fill='red', tags='red')
            elif index < 512:
                self.green.append(int(s))
                if index == 256:
                    self.create_oval(17, 276-int(s)-3, 23, 276-int(s)+3, fill='green', tags='green')
                elif index == 511:
                    self.create_oval(17+3*(index-256), 276-int(s)-3, 23+3*(index-256), 276-int(s)+3, fill='green', tags='green')
                elif index > 256:
                    self.create_line(17+3*(index-256), 276-self.green[-2], 20+3*(index-256), 276-self.green[-1], fill='green', tags='green')
            else:
                self.blue.append(int(s))
                if index == 512:
                    self.create_oval(17, 276-int(s)-3, 23, 276-int(s)+3, fill='blue', tags='blue')
                elif index == 767:
                    self.create_oval(17+3*(index-512), 276-int(s)-3, 23+3*(index-512), 276-int(s)+3, fill='blue', tags='blue')
                elif index > 512:
                    self.create_line(17+3*(index-512), 276-self.blue[-2], 20+3*(index-512), 276-self.blue[-1], fill='blue', tags='blue')  
            index += 1
        f.close()

    def onMove(self, event):
        if self.drawing:
            if self.current_draw == []:
                self.delete('temp-circle')
                self.create_oval(17, event.y-3, 23, event.y+3, fill=self.current_color, tags='temp-circle')
            else:
                x, y = self.current_draw[-1]
                if event.y > 276:
                    event.y = 276
                elif event.y < 20:
                    event.y = 20
                self.delete('temp-line')
                if event.x > 788:
                    self.create_line(x, y, 788, event.y, fill=self.current_color, tags='temp-line')
                    self.create_oval(785, event.y-3, 791, event.y+3, fill=self.current_color, tags='temp-line')
                else:
                    self.create_line(x, y, event.x, event.y, fill=self.current_color, tags='temp-line')

    def onClick(self, event):
        if self.drawing:
            if self.current_draw == []:
                self.delete('temp-circle')
                self.create_oval(17, event.y-3, 23, event.y+3, fill=self.current_color, tags=self.current_color)
                self.current_draw.append((20, event.y))
            else:
                self.delete('temp-line')
                x, y = self.current_draw[-1]
                if event.x > 788:
                    self.create_line(x, y, 788, event.y, fill=self.current_color, tags=self.current_color)
                    self.create_oval(785, event.y-3, 791, event.y+3, fill=self.current_color, tags=self.current_color)
                    self.current_draw.append((event.x, event.y))
                    self.finishDrawing()
                else:
                    self.create_line(x, y, event.x, event.y, fill=self.current_color, tags=self.current_color)
                    self.current_draw.append((event.x, event.y))
        else:
            if event.y < 400 and event.y > 276:
                if event.x > 20 and event.x < 276:
                    self.drawing = True
                    self.current_color = 'red'
                    self.delete('selector')
                    self.delete('red')
                    self.create_rectangle(20, 276, 276, 295, fill='red3', tags='selector')
                    self.create_rectangle(276, 276, 532, 295, fill='dark green', tags='selector')
                    self.create_rectangle(532, 276, 788, 295, fill='dark blue', tags='selector')
                elif event.x > 276 and event.x < 532:
                    self.drawing = True
                    self.current_color = 'green'
                    self.delete('selector')
                    self.delete('green')
                    self.create_rectangle(20, 276, 276, 295, fill='dark red', tags='selector')
                    self.create_rectangle(276, 276, 532, 295, fill='light green', tags='selector')
                    self.create_rectangle(532, 276, 788, 295, fill='dark blue', tags='selector')
                elif event.x > 532 and event.x < 788:
                    self.drawing = True
                    self.current_color = 'blue'
                    self.delete('selector')
                    self.delete('blue')
                    self.create_rectangle(20, 276, 276, 295, fill='dark red', tags='selector')
                    self.create_rectangle(276, 276, 532, 295, fill='dark green', tags='selector')
                    self.create_rectangle(532, 276, 788, 295, fill='light blue', tags='selector')

    def finishDrawing(self):
        self.drawing = False
        if self.current_color == 'red':
            save = self.red = []
        elif self.current_color == 'green':
            save = self.green = []
        elif self.current_color == 'blue':
            save = self.blue = []
        for a in range(0, 256):
            for b in range(1,len(self.current_draw)):
                if self.current_draw[b][0] >= 3*a:
                    x0,y0 = self.current_draw[b-1]
                    x1,y1 = self.current_draw[b]
                    x0, x1 = x0/3, x1/3
                    save.append(276 - (a * (y1 - y0)/(x1 - x0) + y0))
                    break
        self.current_color = 'none'
        self.current_draw = []
        self.delete('selector')
        self.create_rectangle(20, 276, 276, 295, fill='red', tags='selector')
        self.create_rectangle(276, 276, 532, 295, fill='green', tags='selector')
        self.create_rectangle(532, 276, 788, 295, fill='blue', tags='selector')

    def __init__(self, master):
        Canvas.__init__(self, master, height=300, width=808)
        self.current_color = 'none'
        self.drawing = False
        self.current_draw = []
        self.red = []
        self.green = []
        self.blue = []
        self.readFromColorFile()
        self.bind('<Motion>', self.onMove)
        self.bind('<1>', self.onClick)

        ## draw axes
        self.create_line(20, 276, 788, 276, tags='axis')
        self.create_line(20, 20, 20, 276, tags='axis')

        ## draw color_selection
        self.create_rectangle(20, 276, 276, 295, fill='red', tags='selector')
        self.create_rectangle(276, 276, 532, 295, fill='green', tags='selector')
        self.create_rectangle(532, 276, 788, 295, fill='blue', tags='selector')

class ColorMaster(Frame):

    def onSave(self):
        self.pane.updateColorFile()
        if self.link:
            self.link.scaleChanged(None)

    def __init__(self, master, link):
        Frame.__init__(self, master, height=300, width=800)
        self.pane = ColorPane(self)
        self.pane.pack()
        
        self.save = Button(self, text='Save as Color Map', command=self.onSave)
        self.save.pack()
        
        self.link = link
        
class Menubar(Menu):
    
    def ChangeColors(self):
        top = Toplevel()
        top.title("Color Map Editor")
        cm = ColorMaster(top, self.link)
        cm.pack()
    
    def __init__(self, master, link=None):
        Menu.__init__(self, master)
        colormenu = Menu(self, tearoff=0)
        colormenu.add_command(label="Change Colors...", command=self.ChangeColors)
        self.add_cascade(label='Colors', menu=colormenu)
        
        self.link = link


if __name__ == '__main__':
    root = Tk()
    root.title('Menz Fractal')
    mf = mainFrame(root)
    mf.pack()
    mf.scaleChanged(None)
    
    menubar = Menubar(root, mf)
    root.config(menu=menubar)
    
    root.mainloop()
