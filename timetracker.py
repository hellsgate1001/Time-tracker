from models import *
from timetrackerui import *
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query


engine = create_engine('mysql://tracker:X6AbqNhiulEyMHo5F71L@79.125.121.165/timesheet')
Session = sessionmaker(bind=engine)
session = Session()


root = Tk()

"""
User needs to log in before they can do anything
"""
if __name__ == '__main__':
    timetracker = LoginForm(parent=root)
    timetracker.mainloop()

"""login_form = LoginForm(master=root)
login_form.master.title('Authenticate')
login_form.mainloop()

timetracker = AddTask(master=root)
timetracker.master.title("Matador Time Tracking")
timetracker.mainloop()"""
