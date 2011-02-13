from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
#from sqlalchemy import Sequence
#from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://tracker:X6AbqNhiulEyMHo5F71L@79.125.121.165/timesheet')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class UserCategory(Base):
    __tablename__ = 'user_category'

    id = Column(Integer, primary_key=True)
    category = (Column, String(40))

    def __init__(self, category):
        self.name = category

    def __repr__(self):
        return "<UserCategory('%s')>" % (self.category)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = (Column, String(255))
    first_name = (Column, String(40))
    surname = (Column, String(40))
    password = (Column, String(255))
    user_category = (Column, Integer)

    def __init__(self, email, first_name, surname, password, user_category):
        self.email = email
        self.first_name = first_name
        self.surname = surname
        self.password = password
        self.user_category = user_category

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.email, self.first_name, self.surname)


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
        self.start = datetime.datetime()

    def __repr__(self):
        return "<UserTask('%s','%s')>" % (str(self.user), str(self.task))



user_cat = UserCategory('Admin')
session.add(user_cat)
new_cat = session.query(UserCategory).filter_by(category='Admin').first()
