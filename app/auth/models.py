from sqlalchemy import Table, MetaData, func, text
from app import db
import traceback
from flask_login import UserMixin

class User(UserMixin):
    pass

def basic():
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    projects = Table('projects', meta, autoload=True)
    conn.execute(projects.insert(), name='test')

    a = projects.select(projects.c.name == 'test').execute()
    for aa in a: print(aa)

    a = projects.select(projects.c.name == 'test').execute().first()
    print(a)

def select_user_by_email(email):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()
    res = dict(res)
    if res is None:
        return None
    else:
        user = User()

        user.id = res['id']
        user.name = res['name']
        user.email = res['email']

        return user

def verify_password(password, uid):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    #: user의 비밀번호와 입력된 hash_pwd가 일치하는지 확인
    res = u.select()

    if res is True:
        return True
    else:
        return False

def select_user_by_uid(uid):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT id, name, email FROM `marocat v1.1`.users WHERE uid = :uid;"""), uid=uid).fetchone()
    user = dict(res)
    return user
