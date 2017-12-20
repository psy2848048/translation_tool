from sqlalchemy import Table, MetaData
from app import db

def select_word(text):
    conn = db.engine.connect()
    words = conn.execute("SELECT id as word_id, origin_lang, trans_lang, origin_text, trans_text FROM marocat.word_memory WHERE is_deleted = FALSE AND (origin_text = '{}' OR trans_text = '{}');".format(text, text))

    # meta = MetaData(bind=db.engine)
    # wm = Table('word_memory', meta, autoload=True)
    # words = wm.select(wm.c.is_deleted==False).execute()
    return words
