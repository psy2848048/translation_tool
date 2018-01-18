from sqlalchemy import Table, MetaData, func, text
from app import db
import traceback
import io
import csv
from datetime import datetime


def select_termbase(page, rows):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)

    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.termbase WHERE is_deleted = FALSE;""")).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT id as tid, origin_lang, trans_lang, origin_text, trans_text FROM `marocat v1.1`.termbase
                                 WHERE is_deleted = FALSE
                                 LIMIT :row_count OFFSET :offset;"""), row_count=rows, offset=rows * (page - 1))
    terms = [dict(res) for res in results]

    return terms, total_cnt


def insert_term(origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)

    try:
        res = conn.execute(tb.insert(), origin_lang=origin_lang, trans_lang=trans_lang
                           , origin_text=origin_text, trans_text=trans_text)
        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def insert_term_csv_file(csv_file, origin_lang, trans_lang):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    tb = Table('termbase', meta, autoload=True)

    file = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
    data = csv.reader(file)

    try:
        for row in data:
            #: CSV 파일 형식이 `원문언어, 번역언어, 원문단어, 번역단어`순인 경우
            if len(row) == 4:
                res = conn.execute(tb.insert(), origin_lang=row[0], trans_lang=row[1]
                                   , origin_text=row[2], trans_text=row[3])
                if res.rowcount != 1:
                    trans.rollback()
                    return False

            #: CSV 파일 형식이 `원문단어, 번역단어`순인 경우
            elif len(row) == 2:
                res = conn.execute(tb.insert(), origin_lang=origin_lang, trans_lang=trans_lang
                                   , origin_text=row[0], trans_text=row[1])
                if res.rowcount != 1:
                    trans.rollback()
                    return False
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
        res = conn.execute(tb.update(tb.c.id == tid), origin_lang=origin_lang, trans_lang=trans_lang
                           , origin_text=origin_text, trans_text=trans_text, update_time=datetime.utcnow())
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

    try:
        res = conn.execute(tb.update(tb.c.id == tid), is_deleted=True, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False
