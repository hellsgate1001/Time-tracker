#from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
#from sqlalchemy import Sequence
#from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserCategory(Base):
    __tablename__ = 'user_category'

    id = Column(Integer, primary_key=True)
    category = (Column, String(40))

    def __init__(self, category):
        self.name = category

    def __repr__(self):
        return "<UserCategory('%s')>" % (category)


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
        return "<User('%s','%s','%s')>" % (email, first_name, surname)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Project('%s')>" % (name)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    project = Column(Integer)

    def __init__(self, name, project):
        self.name = name
        self.project = project

    def __repr__(self):
        return "<Task('%s','%s')>" % (name, str(project))
