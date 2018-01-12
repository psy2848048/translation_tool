from sqlalchemy import Table, MetaData
from app import db
import traceback
import hashlib

def insert_user(name, email, password):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    try:
        conn.execute(u.insert(), name=name, email=email, password=password)
        return True
    except:
        traceback.print_exc()
        return False
