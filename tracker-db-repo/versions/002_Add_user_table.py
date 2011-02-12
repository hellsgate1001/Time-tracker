from sqlalchemy import *
from migrate import *
from migrate.changeset import *

meta = MetaData()
user_category = Table('user_category', meta)

user = Table('user', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String(255)),
    Column('first_name', String(40)),
    Column('surname', String(40)),
    Column('password', String(255)),
    Column('user_category', Integer, ForeignKey("user_category.id")),
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    user.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user.drop()


"""
    ForeignKeyConstraint(
                    ['user_category'],
                    ['user_category.id'],
                    onupdate="CASCADE", ondelete="SET NULL"
        )
"""