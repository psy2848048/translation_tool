from sqlalchemy import Table, MetaData, text
from app import db, common
import traceback
import io
import csv
from datetime import datetime


def select_trans_memory(uid, origin_lang, trans_lang, page, rows):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.translation_memory tm
                            JOIN user_tmlist ut ON ut.tm_id = tm.id
                            WHERE user_id = :uid AND origin_lang = :ol AND trans_lang = :tl AND tm.is_deleted = FALSE ;""")
                       , uid=uid, ol=origin_lang, tl=trans_lang).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT tm.id as tmid, origin_lang, trans_lang, origin_text, trans_text 
                                  FROM `marocat v1.1`.translation_memory tm
                                  JOIN user_tmlist ut ON ut.tm_id = tm.id
                                  WHERE ut.user_id = :uid AND origin_lang = :ol AND trans_lang = :tl
                                        AND tm.is_deleted = FALSE
                                  ORDER BY tm.id DESC 
                                  LIMIT :row_count OFFSET :offset;""")
                           , uid=uid, ol=origin_lang, tl=trans_lang, row_count=rows, offset=rows * (page - 1))
    tm = [dict(res) for res in results]

    return tm, total_cnt


def insert_trans_memory_csv_file(uid, csv_file, origin_lang, trans_lang):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)
    ut = Table('user_tmlist', meta, autoload=True)

    # file = TextIOWrapper(csv_file)
    file = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
    data = csv.reader(file)

    try:
        for row in data:
            #: CSV 파일 형식이 `원문언어, 번역언어, 원문단어, 번역단어`순인 경우
            if len(row) == 4:
                origin_hash = common.create_md5_hash(row[2])
                trans_hash = common.create_md5_hash(row[3])
                res = conn.execute(tm.insert(), origin_lang=row[0], trans_lang=row[1],
                                   origin_hash=origin_hash, trans_hash=trans_hash,
                                   origin_text=row[2], trans_text=row[3])
                tmid = res.lastrowid
                conn.execute(ut.insert(), user_id=uid, tm_id=tmid)
            #: CSV 파일 형식이 `원문단어, 번역단어`순인 경우
            elif len(row) == 2:
                origin_hash = common.create_md5_hash(row[0])
                trans_hash = common.create_md5_hash(row[1])
                res = conn.execute(tm.insert(), origin_lang=origin_lang, trans_lang=trans_lang,
                                   origin_hash=origin_hash, trans_hash=trans_hash,
                                   origin_text=row[0], trans_text=row[1])
                tmid = res.lastrowid
                conn.execute(ut.insert(), user_id=uid, tm_id=tmid)
            else:
                trans.rollback()
                return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


# def insert_trans_memory(origin_lang, trans_lang, origin_text, trans_text):
#     conn = db.engine.connect()
#     trans = conn.begin()
#     meta = MetaData(bind=db.engine)
#     tm = Table('translation_memory', meta, autoload=True)
#
#     try:
#         res = conn.execute(tm.insert(), origin_lang=origin_lang, trans_lang=trans_lang
#                            , origin_text=origin_text, trans_text=trans_text)
#         if res.rowcount != 1:
#             trans.rollback()
#             return False
#
#         trans.commit()
#         return True
#     except:
#         traceback.print_exc()
#         trans.rollback()
#         return False


def update_trans_memory(tmid, origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    try:
        origin_hash = common.create_md5_hash(origin_text)
        trans_hash = common.create_md5_hash(trans_text)
        res = conn.execute(tm.update(tm.c.id == tmid), origin_lang=origin_lang, trans_lang=trans_lang,
                           origin_hash=origin_hash, trans_hash=trans_hash,
                           origin_text=origin_text, trans_text=trans_text, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return False, None
        params = res.last_updated_params()
        updated_tm = {
            'tmid': params['id_1'],
            'origin_lang': params['origin_lang'],
            'trans_lang': params['trans_lang'],
            'origin_text': params['origin_text'],
            'trans_text': params['trans_text']
        }

        trans.commit()
        return True, updated_tm
    except:
        traceback.print_exc()
        trans.rollback()
        return False, None


def delete_trans_memory(tmid):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    try:
        res1 = conn.execute(tm.update(tm.c.id == tmid), is_deleted=True, update_time=datetime.utcnow())
        if res1.rowcount != 1:
            trans.rollback()
            return False, -1
        params = res1.last_updated_params()
        updated_tmid = params['id_1']

        trans.commit()
        return True, updated_tmid
    except:
        traceback.print_exc()
        trans.rollback()
        return False, -1
