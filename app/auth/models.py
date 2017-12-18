from sqlalchemy import Table, MetaData
from app import db

def basic():
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    projects = Table('projects', meta, autoload=True)
    conn.execute(projects.insert(), name='test')

    a = projects.select(projects.c.name == 'test').execute()
    for aa in a: print(aa)

    a = projects.select(projects.c.name == 'test').execute().first()
    print(a)
