from sqlalchemy import Table, MetaData, exc, text
from app import db, common
import traceback
import hashlib
from datetime import datetime
import re


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

        if res.rowcount != 1:
            print('update_password', res.rowcount)
            trans.rollback()
            return 0

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
        res = conn.execute(u.update().where(u.c.email == email), name=nickname)

        if res.rowcount != 1:
            print('update_nickname', res.rowcount)
            trans.rollback()
            return False

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
        mimetype = re.split('/', picture.content_type)
        pname, purl, is_done = common.upload_photo_to_bytes_on_s3(picture.read(), mimetype[1], email)
        if is_done is False:
            return 2

        res = conn.execute(u.update().where(u.c.email == email), picture_s3key=pname, picture_url=purl)

        if res.rowcount != 1:
            print('update_nickname', res.rowcount)
            trans.rollback()
            return 0

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
