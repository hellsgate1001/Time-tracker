from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
#from sqlalchemy import Sequence
#from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging
from Crypto.Cipher import AES


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

    def __init__(self, email, first_name, surname, password, user_category):
        encrypted_password = self.encobj.encrypt(pad(password))
        self.email = email
        self.first_name = first_name
        self.surname = surname
        self.password = encrypted_password.encode('hex')
        self.user_category = user_category

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.email, self.first_name, self.surname)

    def check_password(self, password):
        password_to_check = self.encobj.encrypt(pad(password))
        if password_to_check.encode('hex') == self.password:
            print 'matched'
        else:
            print 'no match'


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
    start = Column(DateTime)
    end = Column(DateTime)

    def __init__(self, user, task):
        self.user = user
        self.task = task
        self.start = datetime.now()

    def __repr__(self):
        return "<UserTask('%s','%s')>" % (str(self.user), str(self.task))



"""user_cat = UserCategory('Admin')
session.add(user_cat)
new_cat = session.query(UserCategory).filter_by(category='Admin').first()
"""