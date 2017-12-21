from sqlalchemy import Table, MetaData
from app import db
import traceback
import datetime

def select_doc_sentences(doc_id):
    conn = db.engine.connect()
    doc_sentences = conn.execute('select id as sentence_id, project_docs_id as doc_id, origin_text, trans_text, status, trans_type from marocat.doc_sentences where project_docs_id = {} and is_deleted = FALSE;'.format(doc_id))

    # meta = MetaData(bind=db.engine)
    # ds = Table('doc_sentences', meta, autoload=True)
    # doc_sentences = ds.select(ds.c.project_docs_id == doc_id and ds.c.is_deleted == False).execute()

    return doc_sentences



##################################   sentences   ##################################

def update_trans_text_and_type(sentence_id, trans_text, trans_type):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    ds = Table('doc_sentences', meta, autoload=True)

    try:
        conn.execute(ds.update(ds.c.id == sentence_id), trans_text=trans_text, trans_type=trans_type, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

def update_trans_status(sentence_id, status):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    ds = Table('doc_sentences', meta, autoload=True)

    try:
        conn.execute(ds.update(ds.c.id == sentence_id), status=status, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

import re
#from ckonlpy.tag import Twitter
#twit = Twitter()
#
#def devide_by_morpheme(sentence):
#    t1 = re.sub(r"[(]\w+[)]", '', sentence)
#    t2 = re.findall(r'\w+', re.sub(r'\d+', '', t1))
#    texts = [twit.pos(t)[0][0] for t in t2]
#    texts.append(''); texts.insert(0, '')
#    return texts

def devide_by_spacing(self, sentence):
    t1 = re.sub(r"[(]\w+[)]", '', sentence)
    t2 = re.findall(r'\w+', t1)  # ['나는', '18일에', '철수와', '밥을', '먹었다']
    texts = [t for t in t2 if re.match(r'\D+', t) is not None]  # ['나는', '철수와', '밥을', '먹었다']
    # texts.append('')  # ['얼마나', '오래', '비가', '내렸습니까', '']
    # texts.insert(0, '')  # ['', '얼마나', '오래', '비가', '내렸습니까', '']
    return texts

def get_similarity_sentences():
    pass

def search_words_in_sentence():
    pass


##################################   comments   ##################################

def select_sentence_comments(doc_id, sentence_id):
    conn = db.engine.connect()
    comments = conn.execute("""SELECT sc.id, user_id, username, project_docs_id, comment 
                               FROM marocat.sentence_comments sc JOIN marocat.users u ON (sc.user_id = u.id)
                               WHERE sc.is_deleted = FALSE AND project_docs_id = {} AND doc_sentences_id = {};""".format(doc_id, sentence_id))

    # meta = MetaData(bind=db.engine)
    # wm = Table('word_memory', meta, autoload=True)
    # words = wm.select(wm.c.is_deleted==False).execute()
    return comments

def insert_sentence_comment(user_id, doc_id, sentence_id, comment):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    sc = Table('sentence_comments', meta, autoload=True)

    try:
        conn.execute(sc.insert(), user_id=user_id, project_docs_id=doc_id, doc_sentences_id=sentence_id, comment=comment)
        return True
    except:
        traceback.print_exc()
        return False

def update_sentence_comment(comment_id, comment):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    sc = Table('sentence_comments', meta, autoload=True)

    try:
        conn.execute(sc.update(sc.c.id == comment_id), comment=comment, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

def delete_sentence_comment(comment_id):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    sc = Table('sentence_comments', meta, autoload=True)

    try:
        conn.execute(sc.update(sc.c.id == comment_id), is_deleted=True, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return

