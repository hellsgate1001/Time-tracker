from models import *
from timetrackerui import *
from datetime import datetime
import os


BASE_FPATH = os.getcwd() + '/'

root = Tk()
#root.session = session
root.ini_file = BASE_FPATH + 'settings.ini'
root.ini = {}
app = TimeTracker(root)
app.pack()
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


