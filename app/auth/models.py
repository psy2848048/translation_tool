from sqlalchemy import Table, MetaData, func, text
from app import db, common
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


def create_auth_code(email):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    t = Table('token', meta, autoload=True)

    # 입력된 이메일이 가입된 회원인지 확인
    res = conn.execute(text("""SELECT email FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()

    if res is None:
        msg = email + 'is not exist'
        return None, False, msg

    # 가입된 회원이라면 인증코드 만들고 DB에 저장
    try:
        authcode = common.create_token(email)
        issue = email + '님이 비밀번호 복구 요청'
        res = conn.execute(t.insert(), token=authcode, issue=issue)

        if res.rowcount != 1:
            msg = 'Something Wrong!'
            return None, False, msg
    except:
        traceback.print_exc()
        msg = 'Something Wrong!'
        return None, False, msg

    msg = 'OK'
    return authcode, True, msg
