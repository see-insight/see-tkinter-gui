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
        hbar.configure(command=self.scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.scroll_y)
        self.container = self.c.create_rectangle((0, 0, 900, 850), width=0)
        self.show_image()

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


#--------------------------------------TEST FEATURE------------------------------------------------
# Source: https://github.com/foobar167/junkyard/blob/master/manual_image_annotation1/polygon/gui_canvas.py
    
    def scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.c.xview(*args)  # scroll horizontally
        self.show_image()  # redraw the image

    # noinspection PyUnusedLocal
    def scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.c.yview(*args)  # scroll vertically
        self.show_image()  # redraw the image

    def show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.c.coords(self.container)  # get image area
        box_canvas = (self.c.canvasx(0),  # get visible area of the canvas
                      self.c.canvasy(0),
                      self.c.canvasx(self.c.winfo_width()),
                      self.c.canvasy(self.c.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]
        # Convert scroll region to tuple and to integer
        self.c.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            if self.__huge and self.__curr_img < 0:  # show huge image, which does not fit in RAM
                h = int((y2 - y1) / self.imscale)  # height of the tile banŹ
                self.__tile[1][3] = h  # set the tile band height
                self.__tile[2] = self.__offset + self.imwidth * int(y1 / self.imscale) * 3
                self.__image.close()
                self.__image = Image.open(self.path)  # reopen / reset image
                self.__image.size = (self.imwidth, h)  # set size of the tile band
                self.__image.tile = [self.__tile]
                image = self.__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
            else:  # show normal image
                image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
                                    (int(x1 / self.__scale), int(y1 / self.__scale),
                                     int(x2 / self.__scale), int(y2 / self.__scale)))
            #
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), self.__filter))
            imageid = self.c.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            self.c.lower(imageid)  # set image into background
            self.c.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

#---------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    Image_Markup()