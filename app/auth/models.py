from sqlalchemy import Table, MetaData, text, exc
from app import app, db, common
import traceback
from flask_login import UserMixin
from datetime import datetime
import boto3
import requests

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
        if signup_type == 'local':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd)
        elif signup_type == 'facebook':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd, is_certified=True
                               , facebook_id=social_id, picture=picture, conn_facebook_time=datetime.utcnow())
        elif signup_type == 'google':
            res = conn.execute(u.insert(), email=email, name=name, password=hashpwd, is_certified=True
                               , google_id=social_id, picture=picture, conn_google_time=datetime.utcnow())

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


def select_user_by_email(email):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email, is_certified, picture
                              FROM `marocat v1.1`.users 
                              WHERE email = :email AND is_deleted=FALSE ;"""), email=email).fetchone()

    if res is None:
        return None, 0
    elif res['is_certified'] is 0:
        return None, 2
    else:
        user = User()
        user.id = res['email']
        user.nickname = res['name']
        user.picture = res['picture']

        return user, 1


def select_user_by_social_id(social_type, social_id):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id, name, email, picture, facebook_id, google_id
                              FROM `marocat v1.1`.users 
                              WHERE (facebook_id=:fid OR google_id=:gid)AND is_deleted=FALSE ;""")
                       , fid=social_id, gid=social_id).fetchone()

    if res is None:
        return None

    user = User()
    user.id = res['email']
    user.nickname = res['name']
    user.picture = res['picture']

    if social_type == 'facebook':
        user.facebook_id = res['facebook_id']
    elif social_type == 'google':
        user.google_id = res['google_id']

    return user


def select_user_info_by_email(email):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT id, name, email, picture, conn_facebook_time, conn_google_time 
                              FROM `marocat v1.1`.users WHERE email = :email;"""), email=email).fetchone()

    ############################################################################################################

    bucket_name = 'marocat'
    ufilename = 'profile/home_oh3.png'  # DB에 저장할 s3key

    s3 = boto3.client(
        's3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        # aws_session_token=SESSION_TOKEN,
    )

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': ufilename
        }
    )

    res = dict(res)
    # rp = requests.get(url)
    res['picture'] = url

    ############################################################################################################

    if res is None:
        return None
    else:
        user = User()
        user.id = res['email']
        user.info = res
        return user
