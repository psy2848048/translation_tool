from sqlalchemy import Table, MetaData, func, text
from app import db
import traceback
from flask_login import UserMixin

class User(UserMixin):
    def can_login(self, password):
        conn = db.engine.connect()
        res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE id = :uid"""), pwd=password, uid=self.get_id()).fetchone()

        if dict(res)['res'] == 1:
            return True
        else:
            return False

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

def select_user_by_uid(uid):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT id, name, email, profile_photo FROM `marocat v1.1`.users WHERE id = :uid;"""), uid=uid).fetchone()
    res = dict(res)
    if res is None:
        return None
    else:
        user = User()

        user.id = res['id']
        user.name = res['name']
        user.email = res['email']
        user.profile_photo = res['profile_photo']

        return user
