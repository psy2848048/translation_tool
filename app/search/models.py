from app import db
from sqlalchemy import Table, MetaData
from sqlalchemy import text

# def select_word(text):
#     conn = db.engine.connect()
#     words = conn.execute("SELECT id as word_id, origin_lang, trans_lang, origin_text, trans_text FROM marocat.word_memory WHERE is_deleted = FALSE AND (origin_text = '{}' OR trans_text = '{}');".format(text, text))
#
#     # meta = MetaData(bind=db.engine)
#     # wm = Table('word_memory', meta, autoload=True)
#     # words = wm.select(wm.c.is_deleted==False).execute()
#     return words


def select_word(search_text):
    conn = db.engine.connect()
    words = []

    res = conn.execute(text("""SELECT id as word_id, trans_lang, origin_text, trans_text FROM marocat.word_memory 
                               WHERE is_deleted = FALSE AND (origin_text LIKE :noun OR trans_text LIKE :noun );"""), noun='%'+search_text+'%')

    temp = {}
    for r in res:
        if r.trans_lang is not 'ko':
            temp['word_id'] = r.word_id
            temp['origin_text'] = r.trans_text
            temp['trans_text'] = r.origin_text
            words.append(temp)
        else:
            temp['word_id'] = r.word_id
            temp['origin_text'] = r.origin_text
            temp['trans_text'] = r.trans_text
            words.append(temp)

    return words
