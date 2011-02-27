from models import *
from timetrackerui import *
from datetime import datetime

root = Tk()
root.session = Session()

timetracker = LoginForm(parent=root)
timetracker.pack()
root.mainloop()

"""
User needs to log in before they can do anything
"""
#if __name__ == '__main__':
"""timetracker = LoginForm(parent=root)
timetracker.mainloop()

addtask = AddTask(parent=root)
addtask.mainloop()"""
#print root.user.first_name + ' instantiated'

"""login_form = LoginForm(master=root)
login_form.master.title('Authenticate')
login_form.mainloop()"""


