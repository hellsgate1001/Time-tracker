from Tkinter import*


class App(Frame):
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


root = Tk()
timetracker = App(master=root)
timetracker.master.title("Matador Time Tracking")
timetracker.mainloop()
print timetracker.grid_size()
