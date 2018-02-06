from sqlalchemy import Table, MetaData, exc, text
from app import db, common
import traceback
import hashlib
from datetime import datetime


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
