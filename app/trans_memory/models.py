from sqlalchemy import Table, MetaData, func, text
from app import db
import traceback
import csv
from datetime import datetime

def select_trans_memory(page, rows):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    #: 사용자의 총 프로젝트 개수
    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.translation_memory WHERE is_deleted = FALSE;""")).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT id as tmid, origin_lang, trans_lang, origin_text, trans_text FROM `marocat v1.1`.translation_memory
                                  WHERE is_deleted = FALSE
                                  LIMIT :row_count OFFSET :offset;"""), row_count=rows, offset=rows * (page - 1))
    tm = [dict(res) for res in results]

    return tm, total_cnt

def insert_trans_memory(origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    try:
        conn.execute(tm.insert(), origin_lang=origin_lang, trans_lang=trans_lang, origin_text=origin_text, trans_text=trans_text)
        return True
    except:
        traceback.print_exc()
        return False

def insert_trans_memory_csv_file(csv_file, origin_lang, trans_lang):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)
    data = csv.reader(csv_file)

    try:
        for row in data:
            if len(row) == 4:
                conn.execute(tm.insert(), origin_lang=row[0], trans_lang=row[1], origin_text=row[2], trans_text=row[3])
            elif len(row) == 2 and origin_lang is not None and trans_lang is not None:
                conn.execute(tm.insert(), origin_lang=origin_lang, trans_lang=trans_lang, origin_text=row[0], trans_text=row[1])
            else:
                return False
        return True
    except:
        traceback.print_exc()
        return False

def update_trans_memory(tid, origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    try:
        conn.execute(tm.update(tm.c.id == tid), origin_lang=origin_lang, trans_lang=trans_lang, origin_text=origin_text, trans_text=trans_text, update_time=datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

def delete_trans_memory(tid):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    tm = Table('translation_memory', meta, autoload=True)

    try:
        conn.execute(tm.update(tm.c.id == tid), is_deleted=True, update_time=datetime.now())
        return True
    except:
        traceback.print_exc()
        return False
