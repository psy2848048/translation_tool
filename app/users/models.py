from sqlalchemy import Table, MetaData, exc, text
from app import app, db, common
import traceback
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
        #: 원본 사이즈가 (100,100) 이하인 경우는 원본 그대로 저장
        tname = _pname + 'thumbnail' + mtype
        img = Image.open(io.BytesIO(pic))

        imgsize = img.size
        if imgsize[0] > 100 or imgsize[1] > 100:
            img.thumbnail((100, 100), Image.ANTIALIAS)
            b = io.BytesIO()
            img.save(b, format=mimetype[1].upper())
            timg_bytes = b.getvalue()

            S3.upload_fileobj(io.BytesIO(timg_bytes), BUCKET_NAME, tname)
        else:
            S3.upload_fileobj(io.BytesIO(pic), BUCKET_NAME, tname)

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
    tc = Table('trans_comments', meta, autoload=True)

    try:
        #: 번역문댓글 삭제
        conn.execute(tc.update(tc.c.user_id == uid), is_deleted=True, update_time=datetime.utcnow())

        #: 본인이 개설자인 프로젝트와 문서 삭제
        #: project_members, projects, + docs, doc_members, doc_origin_sentences, doc_trans_sentences 삭제
        conn.execute(
            text("""UPDATE `marocat v1.1`.project_members pm
                    LEFT JOIN (projects p, docs d, doc_members dm, doc_origin_sentences os, doc_trans_sentences ts) 
                    ON (pm.project_id=p.id AND pm.project_id=d.project_id AND pm.project_id=dm.project_id AND d.id=os.doc_id AND os.id=ts.origin_id)
                    SET pm.is_deleted=TRUE, pm.update_time=CURRENT_TIMESTAMP
                      , p.is_deleted=TRUE, p.update_time=CURRENT_TIMESTAMP 
                      , d.is_deleted=TRUE, d.update_time=CURRENT_TIMESTAMP 
                      , dm.is_deleted=TRUE, dm.update_time=CURRENT_TIMESTAMP 
                      , os.is_deleted=TRUE, os.update_time=CURRENT_TIMESTAMP 
                      , ts.is_deleted=TRUE, ts.update_time=CURRENT_TIMESTAMP 
                    WHERE pm.user_id=:uid AND is_founder=TRUE;""")
            , uid=uid)

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
