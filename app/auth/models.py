from sqlalchemy import Table, MetaData, text, exc
from app import app, db, common
import traceback
from flask_login import UserMixin
from datetime import datetime
import requests
import re
import io


class User(UserMixin):
    def can_login(self, password):
        conn = db.engine.connect()
        res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE email = :uid"""), pwd=password, uid=self.get_id()).fetchone()

        if res['res'] == 1:
            return True
        else:
            return False


def insert_user(signup_type, name, email, password, social_id, picture):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    hashpwd = common.encrypt_pwd(password)

    try:
        #: 사진이 있는 경우 바이너리로 저장하기
        if len(picture) > 15:
            r = requests.get(picture)
            mimetype = re.split('/', r.headers['Content-Type'])
            pname, purl, is_done = common.upload_photo_to_bytes_on_s3(r.content, mimetype[1], name)
            if is_done is False:
                return 3

        if signup_type == 'local':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd)
        elif signup_type == 'facebook':
                res = conn.execute(u.insert(), email=email, name=name, password=hashpwd
                                   , facebook_id=social_id, conn_facebook_time=datetime.utcnow()
                                   , picture_s3key=pname, picture_url=purl)
        elif signup_type == 'google':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd
                               , google_id=social_id, conn_google_time=datetime.utcnow()
                               , picture_s3key=pname, picture_url=purl)

        if res.rowcount != 1:
            print('DUP! (user is already exist, local)')
            trans.rollback()
            return 2

        is_done = send_email_for_cert_signup(email)
        if is_done is False:
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


def update_user_social_info(social_type, email, social_id):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    try:
        if social_type is 'facebook':
            res = conn.execute(u.update(u.c.email == email), facebook_id=social_id, conn_facebook_time=datetime.utcnow())

        elif social_type is 'google':
            res = conn.execute(u.update(u.c.email == email), google_id=social_id, conn_google_time=datetime.utcnow())

        if res.rowcount != 1:
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


def send_email_for_cert_signup(email):
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


def send_email_for_recovery_pwd(email):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    t = Table('token', meta, autoload=True)
    u = Table('users', meta, autoload=True)

    try:
        #: 16자리 인증코드 생성
        new_pwd = common.create_token(email, size=16)
        res = conn.execute(t.insert(), token=new_pwd, issue_to=email, memo=email+'님이 비밀번호 찾기 요청')
        if res.rowcount != 1:
            print('Wrong! (create_token or insert_token)')
            trans.rollback()
            return False

        #: 변경된 비밀번호로 바꾸기
        hash_new_pwd = common.encrypt_pwd(new_pwd)
        res = conn.execute(u.update(whereclause=(u.c.email == email)), password=hash_new_pwd, update_time=datetime.utcnow())
        if res.rowcount != 1:
            print('Wrong! (update_user_password)')
            trans.rollback()
            return False

        #: 인증코드 이메일 보내기
        title = 'MaroCat에서 새로운 비밀번호를 발급했습니다'
        with open('app/static/front/user/find_pass_email.html', 'r') as f:
            file = f.read()

        content = file.format(password=new_pwd, email=email)
        is_done = common.send_mail(email, title, content)

        if is_done is True:
            trans.commit()
            return True
        else:
            print('Wrong! (send_mail)')
            trans.rollback()
            return False
    except:
        print('Wrong! (send_email_for_recovery_pwd)')
        traceback.print_exc()
        trans.rollback()
        return False


def cert_local_user(email, cert_token):
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
        res = conn.execute(u.update(u.c.email == email), is_certified=True, update_time=datetime.utcnow())

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


def select_user(input_type, input_id):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email, facebook_id, google_id, is_certified, picture_url
                              FROM `marocat v1.1`.users 
                              WHERE (email=:input_id OR facebook_id=:input_id OR google_id=:input_id) 
                              AND is_deleted=FALSE ;"""), input_id=input_id).fetchone()

    if res is None:
        return None, 0
    elif res['is_certified'] is 0:
        return None, 2
    else:
        user = User()
        user.id = res['email']
        user.idx = res['id']
        user.nickname = res['name']
        user.picture = res['picture_url']

        if input_type == 'facebook':
            user.facebook_id = res['facebook_id']
        elif input_type == 'google':
            user.google_id = res['google_id']

        return user, 1


def select_user_info_by_email(email):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT id, name, email, picture_url as picture
                                    , conn_facebook_time, conn_google_time
                              FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()

    if res is None:
        return None
    else:
        user = User()
        user.id = res['email']
        user.info = dict(res)
        return user
