from sqlalchemy import Table, MetaData, text
from app import db, common
import traceback
import io
import csv
from datetime import datetime


def select_termbase(uid, origin_lang, trans_lang, page, rows):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)

    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.termbase tb
                              JOIN user_tblist ut ON ut.tb_id = tb.id
                              WHERE ut.user_id = :uid AND origin_lang = :ol AND trans_lang = :tl 
                                AND tb.is_deleted = FALSE ;""")
                       , uid=uid, ol=origin_lang, tl=trans_lang).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT tb.id as tid, origin_lang, trans_lang, origin_text, trans_text 
                                  FROM `marocat v1.1`.termbase tb
                                  JOIN user_tblist ut ON ut.tb_id = tb.id
                                  WHERE ut.user_id = :uid AND origin_lang = :ol AND trans_lang = :tl
                                        AND tb.is_deleted = FALSE
                                  ORDER BY tb.id DESC 
                                  LIMIT :row_count OFFSET :offset;""")
                           , uid=uid, ol=origin_lang, tl=trans_lang, row_count=rows, offset=rows * (page - 1))
    terms = [dict(res) for res in results]

    return terms, total_cnt


def insert_term(uid, origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)
    ut = Table('user_tblist', meta, autoload=True)

    try:
        origin_hash = common.create_md5_hash(origin_text)
        trans_hash = common.create_md5_hash(trans_text)
        res = conn.execute(tb.insert(), origin_lang=origin_lang, trans_lang=trans_lang,
                           origin_hash=origin_hash, trans_hash=trans_hash,
                           origin_text=origin_text, trans_text=trans_text)
        if res.rowcount != 1:
            trans.rollback()
            return False, -1

        tid = res.lastrowid
        conn.execute(ut.insert(), user_id=uid, tb_id=tid)

        trans.commit()
        return True, tid
    except:
        traceback.print_exc()
        trans.rollback()
        return False, -1


def insert_term_csv_file(uid, csv_file, origin_lang, trans_lang):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)
    ut = Table('user_tblist', meta, autoload=True)

    file = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
    data = csv.reader(file)

    try:
        for row in data:
            #: CSV 파일 형식이 `원문언어, 번역언어, 원문단어, 번역단어`순인 경우
            if len(row) == 4:
                origin_hash = common.create_md5_hash(row[2])
                trans_hash = common.create_md5_hash(row[3])
                res = conn.execute(tb.insert(), origin_lang=row[0], trans_lang=row[1],
                                   origin_hash=origin_hash, trans_hash=trans_hash,
                                   origin_text=row[2], trans_text=row[3])
                tid = res.lastrowid
                conn.execute(ut.insert(), user_id=uid, tb_id=tid)

            #: CSV 파일 형식이 `원문단어, 번역단어`순인 경우
            elif len(row) == 2:
                origin_hash = common.create_md5_hash(row[0])
                trans_hash = common.create_md5_hash(row[1])
                res = conn.execute(tb.insert(), origin_lang=origin_lang, trans_lang=trans_lang,
                                   origin_hash=origin_hash, trans_hash=trans_hash,
                                   origin_text=row[0], trans_text=row[1])
                tid = res.lastrowid
                conn.execute(ut.insert(), user_id=uid, tb_id=tid)

            else:
                trans.rollback()
                return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def update_term(tid, origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)

    try:
        if None in [origin_lang, trans_lang, origin_text]:
            trans_hash = common.create_md5_hash(trans_text)
            res = conn.execute(tb.update(tb.c.id == tid),
                               trans_text=trans_text, trans_hash=trans_hash, update_time=datetime.utcnow())
        else:
            origin_hash = common.create_md5_hash(origin_text)
            trans_hash = common.create_md5_hash(trans_text)
            res = conn.execute(tb.update(tb.c.id == tid), origin_lang=origin_lang, trans_lang=trans_lang,
                               origin_hash=origin_hash, trans_hash=trans_hash,
                               origin_text=origin_text, trans_text=trans_text, update_time=datetime.utcnow())

        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def delete_term(tid):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)
    ut = Table('user_tblist', meta, autoload=True)

    try:
        res1 = conn.execute(tb.update(tb.c.id == tid), is_deleted=True, update_time=datetime.utcnow())
        if res1.rowcount != 1:
            trans.rollback()
            return False

        res2 = conn.execute(ut.update(ut.c.tb_id == tid), is_deleted=True, update_time=datetime.utcnow())
        if res2.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False
