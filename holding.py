

class Window1(Toplevel):
        def __init__(self, parent=None):
            Toplevel.__init__(self, parent)
            self.parent = parent
            #self.config(width=300, height=200, bg='red')
            #self.deiconify()
            self.grid_propagate()
            self.loginform = LoginForm(self)


class LoginForm(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
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
        self.email_label = Label(self)
        self.email_label.config(text='Email Address')
        self.email_label.grid(row=1)

        self.email_input = Entry(self)
        self.email_input.config(text='')
        self.email_input.grid(row=2, padx=13)

        self.password_label = Label(self)
        self.password_label.config(text='Password')
        self.password_label.grid(row=1, column=1)

        self.password_input =Entry(self)
        self.password_input.config(text='', show='*')
        self.password_input.grid(row=2, column=1, padx=13)

        self.continue_button = Button(self)
        self.continue_button.config(text='Log In', height=2, width=12)
        self.continue_button.grid(row=3, pady=4)
        def cb_handler(event, self=self):
            return self._check_login(event, self.email_input.get(),
                self.password_input.get())
        self.continue_button.bind("<Button-1>", cb_handler)

        self.quit_button = Button(self)
        self.quit_button.config(text='Quit', height=2, width=12,
            command=self._clear_frame())
        self.quit_button.grid(row=3, column=1, pady=4)

    def _check_login(self, event, email, password):
        if email == '':
            print 'You forgot the email address'
        if password == '':
            print 'You forgot the password'

        q = self.parent.session.query(User)
        u = q.filter(User.email==email)

        if u.count() == 1:
            if u[0].check_password(password):
                self.parent.user = u[0]
                self.grid_remove()
                print 'found'
            else:
                print 'no match'


    def _clear_frame(self):
        self.pack_forget()




class AddTask(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.config(
            width=500,
            height=200
        )
        self.pack()
        # grid_propagate makes sure the frame keeps the dims set above
        self.grid_propagate(0)
        self.create_widgets()
        self.parent = parent

    def create_widgets(self):
        # Initial form has three controls:
        # 1. Task title
        # 2. Project name
        # 3. Staart self
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
            return self._start_task(event, self.task_input.get(), self.project_input.get())
        self.start_button.bind("<Button-1>", sb_handler)

        self.quit_button = Button(self)
        self.quit_button.config(
            text='Quit',
            command=self.quit
        )
        self.quit_button.grid()

    def _start_task(self, event, task, project):
        """
        Add a new task to the user_task table, checking if it exists first and
        creating it in the task table if necessary
        """
        task_q = self.parent.session.query(Task)
        tasks = task_q.filter(name=task).filter(project==project_obj.id)
        project_q = self.parent.session.query(Project)
        project_obj = project_q.filter(name==project)
        task = Task(task, project_obj.id)
        self.parent.session.add()
        self.parent.session.commit()