from sqlalchemy import Table, MetaData
from app import db
import traceback
import datetime

def select_word_memory():
    conn = db.engine.connect()
    words = conn.execute('SELECT id as word_id, origin_lang, trans_lang, origin_text, trans_text FROM marocat.word_memory WHERE is_deleted = FALSE;')

    # meta = MetaData(bind=db.engine)
    # wm = Table('word_memory', meta, autoload=True)
    # words = wm.select(wm.c.is_deleted==False).execute()
    return words

def insert_word_memory(origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    wm = Table('word_memory', meta, autoload=True)

    try:
        conn.execute(wm.insert(), origin_lang=origin_lang, trans_lang=trans_lang, origin_text=origin_text, trans_text=trans_text)
        return True
    except:
        traceback.print_exc()
        return False

def update_word(word_id, origin_lang, trans_lang, origin_text, trans_text):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    wm = Table('word_memory', meta, autoload=True)

    try:
        conn.execute(wm.update(wm.c.id == word_id), origin_lang=origin_lang, trans_lang=trans_lang, origin_text=origin_text, trans_text=trans_text)
        return True
    except:
        traceback.print_exc()
        return False