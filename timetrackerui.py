from Tkinter import *
from models import *
from models import session
from Crypto.Cipher import AES
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime


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
            #self.root.bind_class(self.email_input, '<FocusIn>', self.highlightemail)
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


class AddTaskPage(Frame):
    project_user_tasks = {}

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.task_label = Label(self)
        self.task_label.config(
            text='Your task',
            anchor='sw'
        )
        self.task_label.grid(
            row=0,
            sticky=N+S+E+W,
            padx=15
        )

        self.task_input = Entry(self)
        self.task_input.config(
            text='',
        )
        self.task_input.grid(
            row=1,
            padx=15
        )

        self.project_label = Label(self)
        self.project_label.config(
            text='Project',
            anchor='sw'
        )
        self.project_label.grid(
            row=0,
            column=1,
            sticky=N+S+E+W,
            padx=15
        )

        projects = get_all_projects()
        option_list = []
        for project in projects:
            option_list.append(project.name)

        self.p_id = StringVar()
        self.p_id.trace('w', self.project_change)
        self.project_input = OptionMenu(self, self.p_id, *option_list)
        self.project_input.config(
            width=10
        )
        self.project_input.grid(
            row=1,
            column=1,
            padx=15
        )

        self.start_button = Button(self)
        self.start_button.config(
            text='Start Task'
        )
        self.start_button.grid(
            row=1,
            column=4,
            padx=15
        )
        def sb_handler(event, self=self):
            return self._start_task(event, self.task_input.get(), self.p_id.get())
        self.start_button.bind("<Button-1>", sb_handler)

        self.quit_button = Button(self)
        self.quit_button.config(
            text='Quit',
            command=self.root.quit_app
        )
        self.quit_button.grid()

        self.logout_button = Button(self)
        self.logout_button.config(
            text='Logout',
            command = self.showlogin
        )
        self.logout_button.grid()

    def showlogin(self):
        self.grid_forget()
        self.root.showlogin()

    def project_change(self, name, index, mode):
        project_name = self.p_id.get()
        #project_q = session.query(Project)
        project = session.query(Project).filter(Project.name==self.p_id.get())[0]
        #task_q = session.query(Task)
        # What tasks does this project have?
        tasks = session.query(Task).filter(Task.project==project.id)

        if tasks.count() > 0:
            self._fill_tasks(tasks)

        print "id - %s - %s" % (project.id, tasks.count())
        print "%s" % (session.query(Task).filter(Task.project==project).as_scalar())

    def _fill_tasks(self, tasks):
        self.task_list = Listbox(self, height=tasks.count())
        for task in tasks:
            self.task_list.insert(END, task.name)
        self.task_list.grid(row=1, column=0, pady=10)

    def _start_task(self, event, task, project):
        """
        Add a new task to the user_task table, checking if it exists first and
        creating it in the task table if necessary
        """
        project_q = session.query(Project)
        project_obj = project_q.filter(Project.name==project)[0]
        task_q = session.query(Task)
        tasks = task_q.filter(Task.name==task).filter(Task.project==project_obj.id)
        if tasks.count() == 0:
            current_task = Task(task, project_obj.id)
            session.add(current_task)
            session.commit()
        else:
            current_task = tasks[0]
        user_task = UserTask(self.root.user.id, current_task.id)
        session.add(user_task)
        session.commit()

class TimeTracker(Frame):
    pages = {}
    buttons = {}

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.get_ini()
        self.pages = self._add_pages()
        self.pages['login'].grid(row=0, column=0, columnspan=2)
        self.buttons['login'] = Button(self, text='Login', command=self.showlogin).grid(row=1, column=1)
        self.buttons['addtask'] = Button(self, text='Add Task', command=self.addtask).grid(row=1, column=0)

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
        ini_file = open(self.root.ini_file, 'rb')
        self.root.ini = {}
        for line in ini_file:
            line_details = line.split('##')
            self.root.ini[line_details[0]] = line_details[1]
        ini_file.close()

    def quit_app(self):
        """
        When quitting the app, write the ini settings to file
        """
        self.set_ini()

        # End any ongoing user task
        user_tasks = session.query(UserTask).filter(UserTask.user==self.user.id).filter(UserTask.end==None)
        if user_tasks.count() > 0:
            for ut in user_tasks:
                print "Found %s" % (ut.id)
                ut.end = datetime.now()
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
