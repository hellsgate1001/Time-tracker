from Tkinter import *
from models import *
from timetracker import session
from Crypto.Cipher import AES


def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    #entry.pack(side=LEFT)
    return entry

def log_in(email_address='', password=''):
    if email_address == '':
        print 'You forgot the email address'
    if password == '':
        print 'You forogt the password'

    q = session.query(User)
    u = q.filter(User.email==email_address)

    if u.count() == 1:
        u = u[0]
        if u.check_password(password):
            print 'match'
        else:
            print 'no match'


class LoginForm(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.config(width=300, height=200)
        self.pack()
        # the '0' in grid_propagate makes sure the frame keeps the dims set above
        self.grid_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        """
        Login form has four controls:
        1. Email
        2. Password
        3. Continue button
        4. Quit button
        """
        email_label = Label(self)
        email_label.config(text='Email Address')
        email_label.grid(row=1)

        email_input = Entry(self)
        email_input.config(text='')
        email_input.grid(row=2, padx=13)

        password_label = Label(self)
        password_label.config(text='Password')
        password_label.grid(row=1, column=1)

        password_input =Entry(self)
        password_input.config(text='', show='*')
        password_input.grid(row=2, column=1, padx=13)

        continue_button = Button(self)
        continue_button.config(text='Log In', height=2, width=12,
            command=lambda: log_in(email_input.get(), password_input.get())
        )
        continue_button.grid(row=3, pady=4)
        quit_button = Button(self)
        quit_button.config(text='Quit', height=2, width=12, command=self.quit)
        quit_button.grid(row=3, column=1, pady=4)



class AddTask(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.config(
            width=500,
            height=200
        )
        self.pack()
        # grid_propagate makes sure the frame keeps the dims set above
        self.grid_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # Initial form has three controls:
        # 1. Task title
        # 2. Project name
        # 3. Staart self
        task_label = Label(self)
        task_label.config(
            text='Your task',
            anchor='sw'
        )
        task_label.grid(
            row=0,
            sticky=N+S+E+W,
            padx=15
        )

        task_input = Entry(self)
        task_input.config(
            text='',
        )
        task_input.grid(
            row=1,
            padx=15
        )

        project_label = Label(self)
        project_label.config(
            text='Project',
            anchor='sw'
        )
        project_label.grid(
            row=0,
            column=1,
            sticky=N+S+E+W,
            padx=15
        )

        option_list = ('Begg', 'Betfair', 'PASMA')
        project_input = OptionMenu(self, StringVar(), *option_list)
        project_input.config(
            width=10
        )
        project_input.grid(
            row=1,
            column=1,
            padx=15
        )

        start_button = Button(self)
        start_button.config(
            text='Start Task'
        )
        start_button.grid(
            row=1,
            column=4,
            padx=15
        )

        quit_button = Button(self)
        quit_button.config(
            text='Quit',
            command=self.quit
        )
        quit_button.grid()


"""root = Tk()
timetracker = TimeTracker(master=root)
timetracker.master.title("Matador Time Tracking")
timetracker.mainloop()"""
