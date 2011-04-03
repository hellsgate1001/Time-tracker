from Tkinter import *
from models import get_all_projects, session
from models import User, Project, UserTask, Task
from addearliertask import AddEarlierTask
from datetime import datetime


class AddTaskPage(Frame):
    project_user_tasks = {}
    current_ut = 0
    project = None

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

        self.task_title = StringVar()
        self.task_input = Entry(self)
        self.task_input.config(
            textvariable=self.task_title
        )
        self.task_input.grid(
            row=1,
            padx=15,
            pady=0
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

        self.projects = get_all_projects()
        self.project_options = []
        for project in self.projects:
            self.project_options.append(project.name)

        self.p_id = StringVar()
        self.p_id.trace('w', self.project_change)
        self.project_input = OptionMenu(self, self.p_id, *self.project_options)
        self.project_input.config(
            width=10
        )
        self.project_input.grid(
            row=1,
            column=1,
            padx=15
        )

        self.task_button_text = StringVar()
        self.task_button_text.set('Start Task')
        self.task_button = Button(self)
        self.task_button.config(
            textvariable=self.task_button_text,
            width=20
        )
        self.task_button.grid(
            row=1,
            column=2,
            padx=15
        )
        def sb_handler(event, self=self):
            return self._task_click(
                event,
                self.task_input.get(),
                self.p_id.get()
            )
        self.task_button.bind("<Button-1>", sb_handler)

        self.earlier_text = StringVar()
        self.earlier_text.set('Add Earlier Task')
        self.earlier_button = Button(self)
        self.earlier_button.config(
            textvariable=self.earlier_text,
            width=20,
            command=self.add_earlier_task
        )
        self.earlier_button.grid(
            row=2,
            column=1,
            sticky=N
        )

        self.quit_button = Button(self)
        self.quit_button.config(
            text='Quit',
            command=self.root.quit_app
        )
        self.quit_button.grid(
            row=3,
            column=1
        )

        self.logout_button = Button(self)
        self.logout_button.config(
            text='Logout',
            command = self.showlogin
        )
        self.logout_button.grid(
            row=3,
            column=2
        )

        self.task_title = StringVar()
        self.task_input = Entry(self)
        self.task_input.config(
            textvariable=self.task_title
        )
        self.task_input.grid(
            row=1,
            padx=15,
            pady=0
        )

        self.start_label = Label(self)
        self.start_label.config(
            text='Time Task Started',
            anchor='sw'
        )

        self.start_text = StringVar()
        self.start_input = Entry(self)
        self.start_input.config(
            textvariable=self.start_text
        )

    def add_earlier_task(self):
        """if self.earlier_text.get() == 'Add Earlier Task':
            self.earlier_text.set('Remove Previous Task')
            self.start_text.set(datetime.now().strftime('%H:%M'))
            self.start_input.grid(
                row=2,
                column=1
            )"""
        w = AddEarlierTask(self)
        w.state('normal')

    def showlogin(self):
        self.grid_forget()
        self.root.showlogin()

    def project_change(self, name, index, mode):
        #project_name = self.p_id.get()
        project = session\
            .query(Project)\
            .filter(Project.name==self.p_id.get())[0]
        # What tasks does this project have?
        tasks = session.query(Task).filter(Task.project==project.id)

        if tasks.count() > 0:
            self._fill_tasks(tasks)

    def _fill_tasks(self, tasks):
        self.task_list = Listbox(self, height=tasks.count())
        for task in tasks:
            self.task_list.insert(END, task.name)
        def tl_handler(event, self=self):
            self.task_title.set(
                self.task_list.get(self.task_list.curselection()[0])
            )
            self.task_list.grid_forget()
        self.task_list.bind('<Double-Button-1>', tl_handler)
        self.task_list.grid(row=2, column=0, rowspan=tasks.count(), sticky=N)

    def _task_click(self, event, task, project):
        if self.task_button_text.get() == 'Start Task':
            self._start_task(task, project)
        else:
            self._end_task(task, project)

    def _end_task(self, task, project):
        ut = session.query(UserTask).get(self.current_ut)
        ut.end_date = datetime.now()
        session.flush()
        self.current_ut = 0

        # Update the text on the button
        self.task_button_text.set('Start Task')

    def _start_task(self, task, project):
        """
        Add a new task to the user_task table, checking if it exists first and
        creating it in the task table if necessary
        """
        project_q = session.query(Project)
        project_obj = project_q.filter(Project.name==project)[0]
        task_q = session.query(Task)
        tasks = task_q.filter(Task.name==task)\
            .filter(Task.project==project_obj.id)
        if tasks.count() == 0:
            current_task = Task(task, project_obj.id)
            session.add(current_task)
            session.commit()
        else:
            current_task = tasks[0]
        user_task = UserTask(self.root.user.id, current_task.id)
        session.add(user_task)
        session.commit()
        self.current_ut = user_task.id

        # Update the text on the button
        self.task_button_text.set('End Task')
