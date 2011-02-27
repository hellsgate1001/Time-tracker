from Tkinter import *
from models import *
from Crypto.Cipher import AES


class LoginForm(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        print self.parent
        self.label = Label(self)
        self.label.config(text='Hello!')
        self.label.grid()

        self.button = Button(self)
        self.button.config(text='World')
        def b_click(event, self=self):
            return self.login_succeeded(event)
        self.button.bind("<Button-1>", b_click)
        self.button.grid(row=1)

    def login_succeeded(self, event):
        self.pack_forget()
        self.parent.addtask.pack()


class AddTask(Frame):
    def __init(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.label = Label(self)
        self.label.config(text='Add Task')
        self.label.grid()


class TimeTracker(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.addtask = AddTask(parent)
        self.loginform = LoginForm(parent=parent)
        self.loginform.pack()


def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    #entry.pack(side=LEFT)
    return entry
