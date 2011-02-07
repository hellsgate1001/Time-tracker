from sqlalchemy import *
from migrate import *

meta = MetaData()

user_category = Table('user_category', meta,
    Column('id', Integer, primary_key=True),
    Column('category', String(40))
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    user_category.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user_category.drop()
