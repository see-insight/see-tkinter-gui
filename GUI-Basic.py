from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import ImageTk, Image, ImageGrab


class Image_Markup(object):

    DEFAULT_COLOR = 'black'
    Image_Width = 900
    Image_Height = 600


    def __init__(self):
        self.root = Tk()
        self.root.title('SEE Image Markup Tool')

        self.point_button = Button(self.root, text='Point Select', command=self.use_point_select)
        self.point_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.browse_button = Button(self.root, text='Browse', command=self.browseFiles)
        self.browse_button.grid(row=0, column=4)

        self.clear_button = Button(self.root, text='Clear All', command=self.clear_all)
        self.clear_button.grid(row=0, column=5)

        self.choose_size_button = Scale(self.root, from_=10, to=50, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6)

        self.save_button = Button(self.root, text='Save', command=self.save_canvas)
        self.save_button.grid(row=0, column=9)

        self.c = Canvas(self.root, bg='white', width=self.Image_Width, height=self.Image_Height)
        self.c.grid(row=1, columnspan=10)

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