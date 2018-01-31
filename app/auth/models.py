from sqlalchemy import Table, MetaData, text, exc
from app import db, common
import traceback
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def can_login(self, password):
        conn = db.engine.connect()
        res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE id = :uid"""), pwd=password, uid=self.get_id()).fetchone()

        if dict(res)['res'] == 1:
            return True
        else:
            return False


def insert_user(name, email, password):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    hashpwd = common.encrypt_pwd(password)

    try:
        res = conn.execute(u.insert(), name=name, email=email, password=hashpwd)

        if res.rowcount != 1:
            print('DUP! (user is already exist)')
            trans.rollback()
            return 2

        #: 사용자에게 인증코드 이메일 보내기
        is_done = send_email_for_local_signup(email)

        if is_done is True:
            trans.commit()
            return True
        else:
            trans.rollback()
            return False
    except exc.IntegrityError:
        print('DUP! (user is already exist)')
        trans.rollback()
        return 2
    except:
        traceback.print_exc()
        trans.rollback()
        return False
    finally:
        conn.close()


def send_email_for_local_signup(email):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    t = Table('token', meta, autoload=True)

    try:
        #: 16자리 인증코드 생성
        cert_token = common.create_token(email, size=16)
        res = conn.execute(t.insert(), token=cert_token, issue_to=email
                           , memo=email+'에게 로컬 회원가입 인증코드 전송')

        if res.rowcount != 1:
            print('Wrong! (create_token or insert_token)')
            trans.rollback()
            return False

        #: 인증코드 이메일 보내기
        title = 'MaroCat 인증 코드입니다.'
        with open('app/static/front/user/email_form.html', 'r') as f:
            file = f.read()

        content = file.format(cert_token=cert_token, email=email)
        is_done = common.send_mail(email, title, content)

        if is_done is True:
            trans.commit()
            return True
        else:
            print('Wrong! (send_mail)')
            trans.rollback()
            False
    except:
        print('Wrong! (send_email_for_local_signup)')
        traceback.print_exc()
        trans.rollback()
        return False


def update_user_local_info(email, cert_token):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    try:
        #: 인증코드 확인
        res = conn.execute(text("""UPDATE `marocat v1.1`.token
                                  SET is_used = TRUE, update_time = CURRENT_TIMESTAMP()
                                  WHERE issue_to=:email AND token=:token""")
                           , email=email, token=cert_token)

        if res.rowcount != 1:
            print('Wrong! (update token, {})'.format(res.rowcount))
            trans.rollback()
            return False

        #: 사용자 인증 정보 수정
        res = conn.execute(u.update(u.c.email == email), cert_local=True, conn_local=True
                           , conn_local_time=datetime.utcnow(), update_time=datetime.utcnow())

        if res.rowcount != 1:
            print('Wrong! (update users, {})'.format(res.rowcount))
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        print('Wrong! (update_user_local_info)')
        traceback.print_exc()
        trans.rollback()
        return False


def select_user_by_email(email):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()
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
    res = conn.execute(text("""SELECT id, name, email FROM `marocat v1.1`.users WHERE id = :uid;"""), uid=uid).fetchone()
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
