from Tkinter import *
from models import session
from models import User, Project, UserTask, Task


class LoginPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.email_label = Label(self)
        self.email_label.config(text='Email Address')
        self.email_label.grid(row=1)

        self.email_input = Entry(self)
        if 'useremail' in self.root.root.ini:
            self.email_input.insert(0, self.root.root.ini['useremail'].strip())
        self.email_input.grid(row=2, padx=13)

        self.password_label = Label(self)
        self.password_label.config(text='Password')
        self.password_label.grid(row=1, column=1)

        def cb_handler(event, self=self):
            return self._check_login(event, self.email_input.get(),
                self.password_input.get())

        self.password_input =Entry(self)
        self.password_input.config(text='', show='*')
        self.password_input.grid(row=2, column=1, padx=13)
        self.password_input.bind("<Return>", cb_handler)
        self.password_input.bind("<KP_Enter>", cb_handler)

        self.continue_button = Button(self)
        self.continue_button.config(text='Log In', height=2, width=12)
        self.continue_button.grid(row=3, pady=4)
        self.continue_button.bind("<Button-1>", cb_handler)
        self.continue_button.bind("<Return>", cb_handler)
        self.continue_button.bind("<KP_Enter>", cb_handler)

        self.quit_button = Button(self)
        self.quit_button.config(text='Quit', height=2, width=12,
            command=self.root.quit_app)
        self.quit_button.grid(row=3, column=1, pady=4)

    def _check_login(self, event, email, password):
        if email == '':
            print 'You forgot the email address'
        if password == '':
            print 'You forgot the password'

        q = session.query(User)
        u = q.filter(User.email==email)

        if u.count() == 1:
            if u[0].check_password(password):
                self.root.user = u[0]
                self.grid_forget()
                self.root.root.ini['useremail'] = email
                self.root.set_ini()
                self.root.addtask()
            else:
                print 'no match'
