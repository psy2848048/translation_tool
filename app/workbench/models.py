from app import db
from sqlalchemy import Table, MetaData, text
import sqlalchemy.exc
import traceback
import datetime

def select_doc(did):
    conn = db.engine.connect()
    doc_sentences = []

    results = conn.execute(text("""SELECT os.doc_id, os.id as origin_id, os.text as origin_text,
                                          ts.id as trans_id, ts.text as trans_text, ts.status, ts.type as trans_type
                                   FROM `marocat v1.1`.doc_origin_sentences os LEFT JOIN doc_trans_sentences ts ON ts.origin_id = os.id AND ts.is_deleted = FALSE
                                   WHERE os.is_deleted = FALSE AND os.doc_id = :did;"""), did=did)
    for res in results:
        doc_sentences.append(dict(res))

    return doc_sentences

def insert_trans(oid, text, trans_type):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    ts = Table('doc_trans_sentences', meta, autoload=True)

    try:
        conn.execute(ts.insert(), origin_id=oid, type=trans_type, text=text)
        return 1
    except sqlalchemy.exc.IntegrityError:
        traceback.print_exc()
        return 2
    except:
        traceback.print_exc()
        return 0

def update_trans(tid, text, trans_type):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    ts = Table('doc_trans_sentences', meta, autoload=True)

    try:
        conn.execute(ts.update(ts.c.id == tid), text=text, type=trans_type, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

def update_trans_status(tid, status):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    ts = Table('doc_trans_sentences', meta, autoload=True)

    try:
        conn.execute(ts.update(ts.c.id == tid), status=status, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return False


##################################   comments   ##################################

def select_trans_comments(tid):
    conn = db.engine.connect()
    comments = []

    results = conn.execute(text("""SELECT c.id as comment_id, trans_id, user_id, text as comment, c.create_time
                                   FROM `marocat v1.1`.comments c JOIN users u ON u.id = c.user_id
                                   WHERE trans_id = :tid AND c.is_deleted = FALSE AND u.is_deleted = FALSE
                                   ORDER BY c.create_time;"""), tid=tid)
    for res in results:
        comments.append(dict(res))

    return comments

def insert_trans_comment(uid, tid, comment):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    c = Table('trans_comments', meta, autoload=True)

    try:
        conn.execute(c.insert(), user_id=uid, trans_id=tid, comment=comment)
        return True
    except:
        traceback.print_exc()
        return False

def delete_trans_comment(cid):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    sc = Table('trans_comments', meta, autoload=True)

    try:
        conn.execute(sc.update(sc.c.id == cid), is_deleted=True, update_time=datetime.datetime.now())
        return True
    except:
        traceback.print_exc()
        return

