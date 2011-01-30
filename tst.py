# using grid() to position a label and a canvas
# tested with Python24   vegaseat    09jun2005

from Tkinter import *

class App(object):
    def __init__(self, root):
        self.root = root
        # create the label
        label1 = Label(root, 
            text="canvas1.create_rectangle(15, 10, 400, 150, outline='red', fill='gray80')")
        # position the label on the form and show it
        """label1.grid(row=0, column=0)
        # create the canvas
        canvas1 = Canvas(root, width=420, height=200)
        # position the canvas on the form and show it
        canvas1.grid(row=1,column=0)
        # now create the recangle on the canvas
        canvas1.create_rectangle(15, 10, 400, 150, outline='red', fill='gray80')
        # position a text at x=100, y=90 so it shows in the rectangle center
        font1 = ('times', 20, 'bold')
        canvas1.create_text(100, 90, anchor=SW, text="Hello World!",
            font=font1, fill='red')"""
        
# create the window's form/root
root = Tk()
# window title text
root.title("Testing Canvas")
# be different, default would be light gray
root.tk_bisque()
# call the class
app  = App(root)
# run program
root.mainloop()
