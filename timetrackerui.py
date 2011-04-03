from Tkinter import *
from models import *
from models import session
from Crypto.Cipher import AES
from loginpage import LoginPage
from addtaskpage import AddTaskPage
from addearliertask import AddEarlierTask


class TimeTracker(Frame):
    pages = {}
    buttons = {}

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.get_ini()
        self.pages = self._add_pages()
        self.user = False
        self.pages['login'].grid(row=0, column=0, columnspan=2)

    def showlogin(self):
        self.pages['login'].grid(row=0, column=0, columnspan=2)

    def removelogin(self):
        self.pages['login'].grid_forget()

    def addtask(self):
        self.pages['addtask'].grid(row=0, column=0, columnspan=2)

    def removeaddtask(self):
        self.pages['addtask'].grid_forget()

    def _add_pages(self):
        all_pages = {}
        all_pages['login'] = LoginPage(self)
        all_pages['addtask'] = AddTaskPage(self)

        return all_pages

    def set_ini(self):
        ini_file = open(self.root.ini_file, 'wb')
        for i in self.root.ini.keys():
            ini_file.write(i + '##' + self.root.ini[i])

        ini_file.close()

    def get_ini(self):
        self.root.ini = {}
        try:
            ini_file = open(self.root.ini_file, 'rb')
            for line in ini_file:
                line_details = line.split('##')
                self.root.ini[line_details[0]] = line_details[1]
            ini_file.close()
        except IOError:
            print 'no such file'

    def quit_app(self):
        """
        When quitting the app, write the ini settings to file
        """
        self.set_ini()

        # End any ongoing user task
        if self.user:
            user_tasks = session\
                .query(UserTask)\
                .filter(UserTask.user==self.user.id)\
                .filter(UserTask.end_date==None)
            if user_tasks.count() > 0:
                for ut in user_tasks:
                    ut.end_date = datetime.now()
                    session.add(ut)
                session.commit()
        self.root.quit()


class LoginForm2(Frame):
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


class AddTask2(Frame):
    def __init(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.label = Label(self)
        self.label.config(text='Add Task')
        self.label.grid()


class TimeTracker2(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.addtask = AddTask(parent)
        self.loginform = LoginForm(parent=parent)
        self.loginform.pack()


"""def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    #entry.pack(side=LEFT)
    return entry"""
