from app import db
from sqlalchemy import Table, MetaData, text
import sqlalchemy.exc
import traceback
from datetime import datetime


def select_doc(did):
    conn = db.engine.connect()
    doc_sentences = []

    results = conn.execute(text("""SELECT os.id as sentence_id, os.text as origin_text
                                        , IF(ts.text is not NULL, ts.text, '') as trans_text
                                        , IF(ts.status is not NULL, ts.status, 0) as trans_status
                                        , IF(ts.type is not NULL, ts.type, 0) as trans_type
                                   FROM `marocat v1.1`.doc_origin_sentences os LEFT JOIN doc_trans_sentences ts ON ts.origin_id = os.id AND ts.is_deleted = FALSE
                                   WHERE os.doc_id = :did AND os.is_deleted = FALSE;"""), did=did)

    doc_sentences = [dict(res) for res in results]
    return doc_sentences


def select_trans_comments(sid):
    conn = db.engine.connect()
    results = conn.execute(text("""SELECT c.id as comment_id, user_id, text as comment, c.create_time
                                   FROM `marocat v1.1`.trans_comments c JOIN users u ON u.id = c.user_id
                                   WHERE origin_id = :sid AND c.is_deleted = FALSE AND u.is_deleted = FALSE
                                   ORDER BY c.create_time;"""), sid=sid)
    comments = [dict(res) for res in results]
    return comments


def export_doc_as_csv(did):
    conn = db.engine.connect()


def insert_or_update_trans(sid, trans_text, trans_type):
    conn = db.engine.connect()
    trans = conn.begin()

    try:
        res = conn.execute(text("""INSERT INTO `marocat v1.1`.doc_trans_sentences
                                   SET origin_id = :oid, text = :trans_text, type = :trans_type
                                   ON DUPLICATE KEY UPDATE origin_id = :oid, text = :trans_text, type = :trans_type, update_time = CURRENT_TIMESTAMP;""")
                           , oid=sid, trans_text=trans_text, trans_type=trans_type)
        print(res.rowcount)
        if res.rowcount not in [1, 2]:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def insert_trans_comment(uid, sid, comment):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    c = Table('trans_comments', meta, autoload=True)

    try:
        res = conn.execute(c.insert(), user_id=uid, origin_id=sid, text=comment)
        if res.rowcount != 1:
            trans.rollback()
            return 0

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def update_sentence_status(sid, status):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    ts = Table('doc_trans_sentences', meta, autoload=True)

    try:
        res = conn.execute(ts.update(ts.c.origin_id == sid), status=status, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return 0

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def delete_trans_comment(cid):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    sc = Table('trans_comments', meta, autoload=True)

    try:
        res = conn.execute(sc.update(sc.c.id == cid), is_deleted=True, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return 0

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return
