from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging
from Crypto.Cipher import AES
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query


engine = create_engine('mysql://tracker:X6AbqNhiulEyMHo5F71L@79.125.121.165/timesheet')
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

BLOCK_SIZE = 32
PADDING = "#"

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

class UserCategory(Base):
    __tablename__ = 'user_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<UserCategory('%s')>" % (self.name)


class User(Base):
    __tablename__ = 'user'
    salt = 'My hat blew off and left my head'

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    first_name = Column(String(40))
    surname = Column(String(40))
    password = Column(String(255))
    user_category = Column(Integer)

    encobj = AES.new(salt, AES.MODE_ECB)

    def __init__(self, email='', first_name='', surname='', password='', user_category=0):
        encrypted_password = self.encobj.encrypt(pad(password))
        self.email = email
        self.first_name = first_name
        self.surname = surname
        self.password = encrypted_password.encode('hex')
        self.user_category = user_category

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.email, self.first_name, self.surname)

    def check_password(self, password_to_check):
        password_to_check = self.encobj.encrypt(pad(password_to_check))
        return password_to_check.encode('hex') == self.password

    def get_latest_task(self):
        ut = session.query(UserTask)\
            .filter(UserTask.user==self.id)\
            .order_by(desc(UserTask.end_date))\
            .limit(1)
        if ut:
            return ut[0]
        return False


def get_all_projects():
    q = session.query(Project)
    projects = q.all()
    return projects


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Project('%s')>" % (self.name)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    project = Column(Integer)

    def __init__(self, name, project):
        self.name = name
        self.project = project

    def __repr__(self):
        return "<Task('%s','%s')>" % (self.name, str(self.project))


class UserTask(Base):
    __tablename__ = 'user_task'

    id = Column(Integer, primary_key=True)
    user = Column(Integer)
    task = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    def __init__(self, user, task):
        self.user = user
        self.task = task
        self.start_date = datetime.now()

    def __repr__(self):
        return "<UserTask('%s','%s')>" % (str(self.user), str(self.task))



"""user_cat = UserCategory('Admin')
session.add(user_cat)
new_cat = session.query(UserCategory).filter_by(category='Admin').first()
"""