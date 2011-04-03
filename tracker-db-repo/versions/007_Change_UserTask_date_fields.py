from sqlalchemy import *
from migrate import *

meta = MetaData()

user_category = Table('user_category', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(40))
)

user = Table('user', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String(255)),
    Column('first_name', String(40)),
    Column('surname', String(40)),
    Column('password', String(255)),
    Column('user_category', Integer, ForeignKey('user_category.id')),
)

project = Table('project', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50))
)

task = Table('task', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('project', Integer, ForeignKey('project.id'))
)

user_task_new = Table('user_task', meta,
    Column('id', Integer, primary_key=True),
    Column('user', Integer, ForeignKey('user.id')),
    Column('task', Integer, ForeignKey('task.id')),
    Column('start_date', DateTime),
    Column('end_date', DateTime)
)

user_task_old = Table('user_task', meta,
    Column('id', Integer, primary_key=True),
    Column('user', Integer, ForeignKey('user.id')),
    Column('task', Integer, ForeignKey('task.id')),
    Column('start', DateTime),
    Column('end', DateTime),
    useexisting=True
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    user_task_old.c.start.alter(name='start_date')
    user_task_old.c.end.alter(name='end_date')

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user_task_new.c.start_date.alter(name='start')
    user_task_new.c.end_date.alter(name='end')
