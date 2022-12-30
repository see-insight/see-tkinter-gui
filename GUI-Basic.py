import os

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from gui_autoscrollbar import AutoScrollbar
from PIL import ImageTk, Image, ImageGrab


class Image_Markup(object):

    DEFAULT_COLOR = 'black'
    Image_Width = 900
    Image_Height = 600


    def __init__(self):
        self.root = Tk()
        self.root.title('SEE Image Markup Tool')
        self.root.maxsize(900, 900)

        top_frame = Frame(self.root,  width=900,  height=50)
        top_frame.pack(side='top',  fill='both',  padx=10,  pady=5,  expand=True)

        self.point_button = Button(top_frame, text='Point Select', command=self.use_point_select)
        self.point_button.pack(side='left', expand = True, fill = BOTH)

        self.brush_button = Button(top_frame, text='Brush', command=self.use_brush)
        self.brush_button.pack(side='left', expand = True, fill = BOTH)

        self.color_button = Button(top_frame, text='Color', command=self.choose_color)
        self.color_button.pack(side='left', expand = True, fill = BOTH)

        self.eraser_button = Button(top_frame, text='Eraser', command=self.use_eraser)
        self.eraser_button.pack(side='left', expand = True, fill = BOTH)

        self.browse_button = Button(top_frame, text='Browse', command=self.browseFiles)
        self.browse_button.pack(side='left', expand = True, fill = BOTH)

        self.clear_button = Button(top_frame, text='Clear All', command=self.clear_all)
        self.clear_button.pack(side='left', expand = True, fill = BOTH)

        self.choose_size_button = Scale(top_frame, from_=10, to=50, orient=HORIZONTAL)
        self.choose_size_button.pack(side='left', expand = True, fill = BOTH)

        self.save_button = Button(top_frame, text='Save', command=self.save_canvas)
        self.save_button.pack(side='left', expand = True, fill = BOTH)

        # bottom_frame = Frame(self.root,  width=900,  height=850)
        # bottom_frame.pack(side='bottom',  fill='both',  padx=10,  pady=5,  expand=True)

        self.imframe = Frame(self.root,  width=900,  height=850)
        self.imframe.pack(side='bottom',  fill='both',  padx=10,  pady=5,  expand=True)

        hbar = AutoScrollbar(self.imframe, orient='horizontal')
        vbar = AutoScrollbar(self.imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')

        self.c = Canvas(self.imframe, bg='white', width=self.Image_Width, height=self.Image_Height)
        self.c.grid(row=0, column=0, sticky='nswe')
        # self.c.pack(side='bottom', expand = True, fill = BOTH)

        self.c.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.brush_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_point_select(self):
        self.activate_button(self.brush_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def clear_all(self):
        self.c.delete("all")

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save_canvas(self):
        x = self.root.winfo_rootx() + self.c.winfo_x()
        y = self.root.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        print('x, y, x1, y1:', x,y,x1,y1)
        ImageGrab.grab().crop((self.c.bbox())).save("/Users/ishaan/Desktop/SavedCanvases/test.png")

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("png files", "*.png"),
                                                        ("jpg files", "*.jpg"),
                                                        ("jpeg files", "*.jpeg")))
        
        img = ImageTk.PhotoImage(Image.open(filename))
        self.Image_Width = img.width()
        self.Image_Height = img.height()
        self.c.create_image(10,10, anchor=NW,image=img)
        self.root.mainloop()



if __name__ == '__main__':
    Image_Markup()