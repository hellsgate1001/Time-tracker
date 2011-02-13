from sqlalchemy import *
from migrate import *

meta = MetaData()

user_task = Table('user_task', meta,
    Column('id', Integer, primary_key=True),
    Column('user', Integer),
    Column('task', Integer),
    Column('start', DateTime),
    Column('end', DateTime)
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    user_task.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user_task.drop()
