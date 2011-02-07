from sqlalchemy import *
from migrate import *
from migrate.changeset import *

meta = MetaData()

user = Table('user', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String(255)),
    Column('first_name', String(40)),
    Column('surname', String(40)),
    Column('password', String(255)),
    Column('user_category', Integer)
)
cons = ForeignKeyConstraint(
    ['user_category'],
    ['user_category.id'],
    name='user_foreign_key_user-category',
    table=user
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    cons.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    cons.drop()
