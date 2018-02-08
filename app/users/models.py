from sqlalchemy import Table, MetaData, exc, text, and_
from app import app, db, common
import traceback
import hashlib
from datetime import datetime
import re
import copy

import boto3
import io
from PIL import Image
S3 = boto3.client(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    # aws_session_token=SESSION_TOKEN,
)
BUCKET_NAME = 'marocat'


def select_user_thumbnail(uid):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT thumbnail_s3key FROM `marocat v1.1`.users WHERE id=:uid;"""), uid=uid).fetchone()
    s3key = res['thumbnail_s3key']
    # a = re.split('.', s3key)
    # mimetype = a[-1]
    # print(a)

    obj = S3.get_object(
        Bucket=BUCKET_NAME,
        Key=s3key
    )
    return io.BytesIO(obj['Body'].read())


def select_user_thumbnail_original(uid):
    conn = db.engine.connect()
    res = conn.execute(text("""SELECT picture_s3key FROM `marocat v1.1`.users WHERE id=:uid;"""), uid=uid).fetchone()

    obj = S3.get_object(
        Bucket=BUCKET_NAME,
        Key=res['picture_s3key']
    )
    return io.BytesIO(obj['Body'].read())


def update_password(email, new_pwd):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    #: 현재 로그인한 사용자의 id로 검색한 패스워드 + 사용자가 입력한 현재 비밀번호가 일치하는지 확인
    # res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE email = :email""")
    #                    , pwd=old_pwd, email=email).fetchone()

    try:
        hash_new_pwd = common.encrypt_pwd(new_pwd)
        res = conn.execute(u.update().where(u.c.email == email), password=hash_new_pwd, update_time=datetime.utcnow())

        # if res.rowcount != 1:
        #     print('update_password', res.rowcount)
        #     trans.rollback()
        #     return 0

        trans.commit()
        return 1
    except exc.IntegrityError:
        print('update_password, IntegrityError')
        trans.rollback()
        return 0
    except:
        traceback.print_exc()
        trans.rollback()
        return 0
    finally:
        conn.close()


def update_nickname(email, nickname):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    try:
        res = conn.execute(u.update().where(u.c.email == email), name=nickname, update_time=datetime.utcnow())

        # if res.rowcount != 1:
        #     print('update_nickname', res.rowcount)
        #     trans.rollback()
        #     return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def update_picture(email, picture):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    try:
        pic = copy.deepcopy(picture.read())

        #: 업로드할 파일 이름짓기
        t = common.create_token(email)
        udate = str(datetime.utcnow().strftime('%Y%m%d%H%M%S'))
        _pname = 'profile/picture-' + udate
        mimetype = re.split('/', picture.content_type)
        mtype = '.' + mimetype[1]

        #: 원본 이미지 저장
        pname = _pname + '-' + mtype
        S3.upload_fileobj(io.BytesIO(pic), BUCKET_NAME, pname)

        #: 썸네일 저장
        img = Image.open(io.BytesIO(pic))
        img.thumbnail((30, 30), Image.ANTIALIAS)
        b = io.BytesIO()
        img.save(b, format=mimetype[1].upper())
        timg_bytes = b.getvalue()

        tname = _pname + 'thumbnail' + mtype
        S3.upload_fileobj(io.BytesIO(timg_bytes), BUCKET_NAME, tname)

        # purl = S3.generate_presigned_url(
        #     ClientMethod='get_object',
        #     Params={
        #         'Bucket': BUCKET_NAME,
        #         'Key': pname
        #     }
        # )
    except:
        print('Wrong! (S3 upload_fileobj)')
        traceback.print_exc()
        return 2

    try:
        res = conn.execute(u.update().where(u.c.email == email), picture_s3key=pname, thumbnail_s3key=tname
                           , update_time=datetime.utcnow())

        # if res.rowcount != 1:
        #     print('update_nickname', res.rowcount)
        #     trans.rollback()
        #     return 0

        trans.commit()
        return 1
    except:
        traceback.print_exc()
        trans.rollback()
        return 0


def delete_user(uid):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)

    u = Table('users', meta, autoload=True)
    p = Table('projects', meta, autoload=True)
    pm = Table('project_members', meta, autoload=True)
    dm = Table('doc_members', meta, autoload=True)
    d = Table('docs', meta, autoload=True)
    tc = Table('trans_comments', meta, autoload=True)

    try:
        #: 번역문댓글 삭제
        conn.execute(tc.update(tc.c.user_id == uid), is_deleted=True, update_time=datetime.utcnow())

        #: 번역문 삭제
        conn.execute(
            text("""UPDATE `marocat v1.1`.doc_trans_sentences ts 
                    JOIN ( doc_origin_sentences os, doc_members dm ) ON ( ts.origin_id = os.id AND os.doc_id = dm.doc_id)
                    SET ts.is_deleted=TRUE, ts.update_time=CURRENT_TIMESTAMP 
                    WHERE user_id = :uid;""")
            , uid=uid)

        #: 원문 삭제
        conn.execute(
            text("""UPDATE `marocat v1.1`.doc_origin_sentences os JOIN doc_members dm ON os.doc_id = dm.doc_id
                    SET os.is_deleted=TRUE, os.update_time=CURRENT_TIMESTAMP 
                    WHERE user_id = :uid;""")
            , uid=uid)

        #: 프로젝트의 문서 삭제
        conn.execute(
            text("""UPDATE `marocat v1.1`.docs d JOIN doc_members dm ON d.id = dm.doc_id
                            SET d.is_deleted=TRUE, d.update_time=CURRENT_TIMESTAMP 
                            WHERE user_id = :uid;""")
            , uid=uid)

        #: 프로젝트 참가자의 문서 권한 삭제
        conn.execute(dm.update(dm.c.user_id == uid), is_deleted=True, update_time=datetime.utcnow())

        #: 프로젝트 삭제 및 프로젝트 참가자에서 삭제
        conn.execute(
            text("""UPDATE `marocat v1.1`.projects p JOIN project_members pm ON p.id = pm.project_id
                    SET p.is_deleted=TRUE, p.update_time=CURRENT_TIMESTAMP
                      , pm.is_deleted=TRUE, pm.update_time=CURRENT_TIMESTAMP 
                    WHERE user_id = :uid;""")
            , uid=uid)
        # res = conn.execute(pm.update(pm.c.user_id == uid), is_deleted=True, update_time=datetime.utcnow())
        # res = conn.execute(p.update(p.c.id == pid), is_deleted=True, update_time=datetime.utcnow())

        #: 사용자 삭제
        res = conn.execute(u.update(u.c.id == uid), is_deleted=True, update_time=datetime.utcnow())
        if res.rowcount != 1:
            print('Wrong (delete/update user)')
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        print('Wrong (delete_user)')
        traceback.print_exc()
        trans.rollback()
        return False
