from sqlalchemy import Table, MetaData, exc, text
from app import db, common
import traceback
import hashlib
from datetime import datetime


def update_password(uid, old_pwd, new_pwd):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    u = Table('users', meta, autoload=True)

    # 1. 현재 로그인한 사용자의 id로 검색한 패스워드 + 사용자가 입력한 현재 비밀번호가 일치하는지 확인
    res = conn.execute(text("""SELECT password = SHA2(:pwd, 512) as res FROM users WHERE id = :uid""")
                       , pwd=old_pwd, uid=uid).fetchone()

    # 2. 일치한다면 새로운 비밀번호로 수정
    if dict(res)['res'] == 1:
        try:
            hash_new_pwd = common.encrypt_pwd(new_pwd)
            res = conn.execute(u.update().where(u.c.id == uid), password=hash_new_pwd, update_time=datetime.utcnow())

            if res.rowcount != 1:
                trans.rollback()
                return False, 461

            trans.commit()
            return True, 200
        except exc.IntegrityError:
            trans.rollback()
            return False, 462
        except:
            traceback.print_exc()
            trans.rollback()
            return False, 461
        finally:
            conn.close()
    else:
        trans.rollback()
        return False, 401
