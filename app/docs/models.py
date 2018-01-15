from app import db, common
from sqlalchemy import Table, MetaData, text, func, and_
import traceback
from datetime import datetime


def select_doc_info(did):
    conn = db.engine.connect()
    result = conn.execute(text("""SELECT id as id, title, status, link, origin_lang, trans_lang, due_date
                                  FROM `marocat v1.1`.docs WHERE id = :did;"""), did=did).fetchone()

    doc_info = dict(result)
    return doc_info


def select_doc_members(did, page, rows):
    conn = db.engine.connect()

    #: 프로젝트 참가자의 총 인원
    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.doc_members dm JOIN users u ON u.id = dm.user_id
                              WHERE doc_id = :did AND dm.is_deleted = FALSE AND u.is_deleted = FALSE;"""), did=did).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT dm.user_id, u.name, u.email, can_read, can_modify, can_delete
                                   FROM `marocat v1.1`.doc_members dm JOIN users u ON u.id = dm.user_id
                                   WHERE dm.doc_id = :did AND dm.is_deleted = FALSE AND u.is_deleted = FALSE
                                   LIMIT :row_count OFFSET :offset;"""), did=did, row_count=rows, offset=rows * (page - 1))
    doc_members = [dict(res) for res in results]

    return doc_members, total_cnt


def update_doc_info(did, title, status, link, origin_lang, trans_lang, due_date):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    d = Table('docs', meta, autoload=True)

    try:
        res = conn.execute(d.update(d.c.id == did), title=title, status=status, link=link
                           , origin_lang=origin_lang, trans_lang=trans_lang, due_date=due_date, update_time=datetime.utcnow())

        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def update_doc_member(did, mid, can_read, can_modify, can_delete):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    dm = Table('doc_members', meta, autoload=True)

    try:
        res = conn.execute(dm.update(and_(dm.c.doc_id == did, dm.c.user_id == mid))
                           , can_read=can_read, can_modify=can_modify, can_delete=can_delete, update_time=datetime.utcnow())

        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False


def delete_doc(did):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)

    dm = Table('doc_members', meta, autoload=True)
    d = Table('docs', meta, autoload=True)

    try:
        res = conn.execute(d.update(d.c.id == did), is_deleted=True, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return False

        res = conn.execute(dm.update(dm.c.doc_id == did), is_deleted=True, update_time=datetime.utcnow())
        if res.rowcount != 1:
            trans.rollback()
            return False

        conn.execute(text("""UPDATE `marocat v1.1`.trans_comments tc JOIN ( doc_trans_sentences ts, doc_origin_sentences os, docs d ) ON ( ts.id = tc.trans_id AND ts.origin_id = os.id AND os.doc_id = d.id)
                            SET tc.is_deleted=TRUE, tc.update_time=CURRENT_TIMESTAMP
                            WHERE doc_id = :did;"""), did=did)
        conn.execute(text("""UPDATE `marocat v1.1`.doc_trans_sentences ts JOIN ( doc_origin_sentences os, docs d ) ON ( ts.origin_id = os.id AND os.doc_id = d.id)
                            SET ts.is_deleted=TRUE, ts.update_time=CURRENT_TIMESTAMP
                            WHERE doc_id = :did;"""), did=did)
        conn.execute(text("""UPDATE `marocat v1.1`.doc_origin_sentences os JOIN docs d ON os.doc_id = d.id
                            SET os.is_deleted=TRUE, os.update_time=CURRENT_TIMESTAMP
                            WHERE doc_id = :did;"""), did=did)

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False
