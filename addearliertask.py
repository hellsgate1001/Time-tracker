from Tkinter import *
from datetime import datetime
from dlgCalendar import tkCalendar
from models import session
from models import User, Project, UserTask, Task


class AddEarlierTask(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.parent = parent

        self.task_label = Label(self)
        self.task_label.config(
            text='Task'
        )
        self.task_label.grid()

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

        self.early_p_id = StringVar()
        self.early_p_id.trace('w', self.project_change)
        self.project_input = OptionMenu(self, self.early_p_id, *self.parent.project_options)
        self.project_input.config(
            width=10
        )
        self.project_input.grid(
            row=1,
            column=1,
            padx=15
        )
        self.add_button = Button(self)
        self.start_label = Label(self)
        self.start_label.config(
            text='Start'
        )
        self.start_label.grid(column=0, row=3)

        self.start_date_text = StringVar()
        self.start_date_text.set(self.parent.root.user.get_latest_task().end_date.strftime('%d/%m/%Y'))
        self.start_date_input = Entry(self)
        self.start_date_input.config(
            textvariable=self.start_date_text
        )
        self.start_date_input.grid(column=1, row=3)
        def sdi_handler(event, self=self):
            tkCalendar(
                self.parent,
                datetime.now().strftime('%Y'),
                datetime.now().strftime('%m'),
                datetime.now().strftime('%d'),
                self.start_date_text
            )
        self.start_date_input.bind('<Double-ButtonPress-1>', sdi_handler)

        self.start_time_text = StringVar()
        self.start_time_text.set(self.parent.root.user.get_latest_task().end_date.strftime('%H:%M'))
        self.start_time_input = Entry(self)
        self.start_time_input.config(textvariable=self.start_time_text)
        self.start_time_input.grid(column=2, row=3)

        self.end_label = Label(self)
        self.end_label.config(
            text='To'
        )
        self.end_label.grid(column=3, row=2)

        self.end_date_text = StringVar()
        self.end_date_text.set(datetime.now().strftime('%d/%m/%Y'))
        self.end_date_input = Entry(self)
        self.end_date_input.config(
            textvariable=self.end_date_text,
            state=DISABLED
        )
        self.end_date_input.grid(column=4, row=3)
        def edi_handler(event, self=self):
            tkCalendar(
                self.parent,
                datetime.now().strftime('%Y'),
                datetime.now().strftime('%m'),
                datetime.now().strftime('%d'),
                self.end_date_text
            )
        self.end_date_input.bind('<Double-ButtonPress-1>', edi_handler)

        self.end_time_text = StringVar()
        self.end_time_text.set(datetime.now().strftime('%H:%M'))
        self.end_time_input = Entry(self)
        self.end_time_input.config(
            textvariable=self.end_time_text,
            state=DISABLED
        )
        self.end_time_input.grid(column=5, row=3)
        self.in_progress_label = Label(self)

        self.in_progress_var = IntVar()
        self.in_progress_input = Checkbutton(self)
        self.in_progress_input.config(
            text='In Progress',
            variable=self.in_progress_var
        )
        self.in_progress_input.grid(column=6, row=3)
        #self.in_progress_input.bind('<ButtonPress-1>', ipi_handler)

    def project_change(self, name, index, mode):
        project = session\
            .query(Project)\
            .filter(Project.name==self.early_p_id.get())[0]
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
