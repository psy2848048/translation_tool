from sqlalchemy import Table, MetaData, text, exc
from app import db, common
import traceback
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def can_login(self, password):
        conn = db.engine.connect()
        res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE email = :uid"""), pwd=password, uid=self.get_id()).fetchone()

        if res['res'] == 1:
            return True
        else:
            return False


def upsert_user(signup_type, name, email, password=None, facebook_id=None):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    if password:
        hashpwd = common.encrypt_pwd(password)

    try:
        if signup_type is 'local':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd)

            if res.rowcount != 1:
                print('DUP! (user is already exist, local)')
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

        elif signup_type is 'facebook':
            res = conn.execute(text("""INSERT INTO `marocat v1.1`.users (email, name, facebook_id, conn_facebook_time)
                                      VALUES (:email, :name, :facebook_id, CURRENT_TIMESTAMP())
                                      ON DUPLICATE KEY UPDATE facebook_id=:facebook_id
                                                            , conn_facebook_time=CURRENT_TIMESTAMP();""")
                               , email=email, name=name, facebook_id=facebook_id)

            if res.rowcount not in [1, 2]:
                trans.rollback()
                return False

            trans.commit()
            return True
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
            return 2

        #: 사용자 인증 정보 수정
        res = conn.execute(u.update(u.c.email == email), cert_local=True
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

    res = conn.execute(text("""SELECT id, name, email, facebook_id, cert_local, conn_local_time
                              FROM `marocat v1.1`.users 
                              WHERE email = :email AND is_deleted=FALSE ;"""), email=email).fetchone()

    if res is None:
        return None, 0

    user = User()
    user.id = res['email']
    user.nickname = res['name']

    if res['conn_local_time'] is None:
        return None, 2
    else:
        return user, 1


def select_user_by_facebook_id(facebook_id):

    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email, facebook_id
                              FROM `marocat v1.1`.users 
                              WHERE facebook_id=:facebook_id AND is_deleted=FALSE ;""")
                       , facebook_id=facebook_id).fetchone()

    if res is None:
        return None
    else:
        user = User()
        user.id = res['email']
        user.nickname = res['name']
        user.facebook_id = res['facebook_id']
        return user


def select_user_info_by_email(email):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT id, name, email
                                    , conn_local_time, conn_facebook_time, conn_google_time
                              FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()
    r = dict(res)

    if res is None:
        return None
    else:
        user = User()
        user.id = r['email']
        user.info = r
        return user
