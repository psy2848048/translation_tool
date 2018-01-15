from app import db, common
from sqlalchemy import Table, MetaData, text, func, and_
import traceback
from datetime import datetime

def select_projects(uid, page, rows):
    conn = db.engine.connect()

    #: 사용자의 총 프로젝트 개수
    res = conn.execute(text("""SELECT count(*) 
                               FROM `marocat v1.1`.project_members pm JOIN projects p ON p.id = pm.project_id
                               WHERE user_id = :uid AND pm.is_deleted = FALSE AND p.is_deleted = FALSE;"""), uid=uid).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT p.id, p.name, p.status, p.create_time, p.due_date
                                          , founder
                                          , IF(progress_percent is not NULL, progress_percent, 0) as progress_percent
                                    FROM `marocat v1.1`.projects p JOIN project_members pm ON pm.project_id = p.id
                                                                  JOIN ( SELECT project_id as pid, user_id as uid, name as founder
                                                                        FROM `marocat v1.1`.project_members pm JOIN ( users u ) ON ( u.id = pm.user_id )
                                                                        WHERE is_founder = True AND u.is_deleted = FALSE ) t2 ON ( t2.pid = p.id )
                                                                  LEFT JOIN ( SELECT d.project_id as pid, CAST(FLOOR(SUM(ts.status) / COUNT(*) * 100) AS CHAR) as progress_percent
                                                                              FROM `marocat v1.1`.doc_trans_sentences ts JOIN ( doc_origin_sentences os, docs d ) ON ( os.doc_id = d.id AND os.id = ts.id )
                                                                              WHERE ts.is_deleted = FALSE AND os.is_deleted = FALSE AND d.is_deleted = FALSE
                                                                              GROUP BY d.project_id ) t1 ON ( t1.pid = p.id ) 
                                    WHERE pm.user_id = :uid AND pm.is_deleted = FALSE AND p.is_deleted = FALSE
                                    ORDER BY p.create_time DESC 
                                    LIMIT :row_count OFFSET :offset;"""), uid=uid, row_count=rows, offset=rows * (page - 1))
    projects = [dict(res) for res in results]

    return projects, total_cnt

def select_project_info(pid):
    conn = db.engine.connect()
    result = conn.execute(text("""SELECT p.id, p.name, p.status, p.create_time, p.due_date,
                                          GROUP_CONCAT(u.name) as project_members,
                                          origin_langs, trans_langs
                                    FROM `marocat v1.1`.projects p JOIN ( project_members pm, users u ) ON ( pm.project_id = p.id AND u.id = pm.user_id )
                                                                   JOIN ( SELECT project_id as pid, group_concat( DISTINCT origin_lang) as origin_langs, group_concat( DISTINCT trans_lang) as trans_langs
                                                                          FROM `marocat v1.1`.docs WHERE is_deleted = FALSE
                                                                          GROUP BY pid ) t1 ON ( t1.pid = p.id )
                                    WHERE p.id = :pid AND p.is_deleted = FALSE AND pm.is_deleted = FALSE AND u.is_deleted = FALSE;"""), pid=pid).fetchone()

    project_info = dict(result)
    return project_info

def select_project_docs(pid, page, rows):
    conn = db.engine.connect()

    #: 프로젝트의 총 문서 개수
    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.docs WHERE project_id = :pid AND is_deleted = FALSE;"""), pid=pid).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT d.id, d.title, d.status, d.link, d.origin_lang, d.trans_lang, d.due_date
                                          , IF(progress_percent is not NULL, progress_percent, 0) as progress_percent
                                   FROM `marocat v1.1`.docs d LEFT JOIN ( SELECT d.id as did, CAST(FLOOR(SUM(ts.status) / COUNT(*) * 100) AS CHAR) as progress_percent
                                                                          FROM `marocat v1.1`.doc_trans_sentences ts JOIN ( doc_origin_sentences os, docs d ) ON ( os.doc_id = d.id AND os.id = ts.id )
                                                                          WHERE ts.is_deleted = FALSE AND os.is_deleted = FALSE
                                                                          GROUP BY d.id ) t1 ON ( t1.did = d.id )
                                   WHERE d.project_id = :pid AND d.is_deleted = FALSE
                                   GROUP BY d.id
                                   ORDER BY d.create_time DESC 
                                   LIMIT :row_count OFFSET :offset"""), pid=pid, row_count=rows, offset=rows * (page - 1))
    project_docs = [dict(res) for res in results]

    return project_docs, total_cnt

def select_project_members(pid, page, rows):
    conn = db.engine.connect()

    #: 프로젝트 참가자의 총 인원
    res = conn.execute(text("""SELECT count(*) FROM `marocat v1.1`.project_members pm JOIN users u ON u.id = pm.user_id
                              WHERE project_id = :pid AND u.is_deleted = FALSE AND pm.is_deleted = FALSE;"""), pid=pid).fetchone()
    total_cnt = res[0]

    results = conn.execute(text("""SELECT pm.user_id, u.name, u.email, can_read, can_modify, can_delete, can_create_doc
                                   FROM `marocat v1.1`.project_members pm JOIN users u ON u.id = pm.user_id
                                   WHERE project_id = :pid AND pm.is_deleted = FALSE AND u.is_deleted = FALSE
                                   LIMIT :row_count OFFSET :offset;"""), pid=pid, row_count=rows, offset=rows * (page - 1))
    project_members = [dict(res) for res in results]

    return project_members, total_cnt


def insert_project(uid, name, due_date):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    p = Table('projects', meta, autoload=True)
    pm = Table('project_members', meta, autoload=True)

    due_date = common.convert_datetime_4mysql(due_date)

    try:
        #: 프로젝트 추가
        res = conn.execute(p.insert(), name=name, due_date=due_date)
        pid = res.lastrowid

        #: 프로젝트 추가한 사람을 프로젝트 참가자에 등록
        conn.execute(pm.insert(), user_id=uid, project_id=pid, is_founder=True,
                                  can_read=True, can_modify=True, can_delete=True, can_create_doc=True)
        return True
    except:
        traceback.print_exc()
        return False

def insert_doc_and_sentences(pid, title, origin_lang, trans_lang, due_date, type, sentences):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    d = Table('docs', meta, autoload=True)
    os = Table('doc_origin_sentences', meta, autoload=True)

    due_date = common.convert_datetime_4mysql(due_date)

    try:
        #: 문서 추가
        res = conn.execute(d.insert(), project_id=pid, title=title, origin_lang=origin_lang, trans_lang=trans_lang, due_date=due_date, type=type)
        did = res.lastrowid

        #: 문서의 문장들 저장
        for sentence in sentences:
            conn.execute(os.insert(), doc_id=did, text=sentence)

        #: 프로젝트 참가자들의 문서 권한 저장
        #  버전1에서는 프로젝트 참가자 모두가 문서내 모든 권한을 갖고있다(True)
        conn.execute(text("""INSERT INTO `marocat v1.1`.doc_members (user_id, project_id, doc_id, can_read, can_modify, can_delete)
                             SELECT user_id, project_id, :did, True, True, True
                             FROM `marocat v1.1`.project_members
                             WHERE project_id = :pid;"""), did=did, pid=pid)

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False

def insert_project_member(pid, uid, can_read, can_modify, can_delete, can_create_doc):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    pm = Table('project_members', meta, autoload=True)

    try:
        conn.execute(pm.insert(), user_id=uid, project_id=pid, is_founder=False,
                                  can_read=can_read, can_modify=can_modify, can_delete=can_delete, can_create_doc=can_create_doc)
        return True
    except:
        traceback.print_exc()
        return False


def update_project_member(pid, mid, can_read, can_modify, can_delete, can_create_doc):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    pm = Table('project_members', meta, autoload=True)

    try:
        conn.execute(pm.update(and_(pm.c.project_id == pid, pm.c.user_id == mid)),
                     can_read=can_read, can_modify=can_modify, can_delete=can_delete, can_create_doc=can_create_doc, update_time=datetime.now())
        return True
    except:
        traceback.print_exc()
        return False

def update_project_info(pid, name, status, due_date):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)
    p = Table('projects', meta, autoload=True)

    due_date = common.convert_datetime_4mysql(due_date)

    try:
        conn.execute(p.update(p.c.id == pid), name=name, status=status, due_date=due_date)
        return True
    except:
        traceback.print_exc()
        return False


def delete_project(pid):
    """
    프로젝트를 삭제한다.
    는 데이터베이스에서 is_deleted를 True로 바꾼다는 의미. 실제로 데이터베이스에서 데이터를 삭제하진 않는다.
    또한, 프로젝트를 삭제하면 프로젝트 참가자, 프로젝트 문서, 프로젝트 참가자의 문서 권한, 문서 댓글 또한 삭제한다.
    -- doc_members, doc_origin_sentences, docs, doc_trans_sentences, project_members, projects, trans_comments
    """
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    p = Table('projects', meta, autoload=True)
    pm = Table('project_members', meta, autoload=True)
    dm = Table('doc_members', meta, autoload=True)
    d = Table('docs', meta, autoload=True)

    try:
        conn.execute(p.update(p.c.id == pid), is_deleted=True, update_time=datetime.now())
        conn.execute(pm.update(pm.c.project_id == pid), is_deleted=True, update_time=datetime.now())
        conn.execute(dm.update(dm.c.project_id == pid), is_deleted=True, update_time=datetime.now())
        conn.execute(d.update(d.c.project_id == pid), is_deleted=True, update_time=datetime.now())
        conn.execute(text("""UPDATE `marocat v1.1`.trans_comments tc JOIN ( doc_trans_sentences ts, doc_origin_sentences os, docs d ) ON ( ts.id = tc.trans_id AND ts.origin_id = os.id AND os.doc_id = d.id)
                             SET tc.is_deleted=TRUE, tc.update_time=CURRENT_TIMESTAMP 
                             WHERE project_id = :pid;
                             UPDATE `marocat v1.1`.doc_trans_sentences ts JOIN ( doc_origin_sentences os, docs d ) ON ( ts.origin_id = os.id AND os.doc_id = d.id)
                             SET ts.is_deleted=TRUE, ts.update_time=CURRENT_TIMESTAMP 
                             WHERE project_id = :pid;
                             UPDATE `marocat v1.1`.doc_origin_sentences os JOIN docs d ON os.doc_id = d.id
                             SET os.is_deleted=TRUE, os.update_time=CURRENT_TIMESTAMP 
                             WHERE project_id = :pid;"""), pid=pid)
        return True
    except:
        traceback.print_exc()
        return False

def delete_project_member(pid, mid):
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    pm = Table('project_members', meta, autoload=True)
    dm = Table('doc_members', meta, autoload=True)

    try:
        #: 프로젝트 참가자 목록에서 삭제
        conn.execute(pm.update(and_(pm.c.project_id == pid, pm.c.user_id == mid)), is_deleted=True, update_time=datetime.now())

        #: 프로젝트 참가자의 문서 권한 목록에서 삭제
        conn.execute(dm.update(and_(dm.c.project_id == pid, dm.c.user_id == mid)), is_deleted=True, update_time=datetime.now())

        #: 프로젝트 참가자가 작성한 댓글 삭제
        conn.execute(text("""UPDATE `marocat v1.1`.trans_comments tc JOIN ( doc_trans_sentences ts, doc_origin_sentences os, docs d ) ON ( ts.id = tc.trans_id AND ts.origin_id = os.id AND os.doc_id = d.id)
                             SET tc.is_deleted=TRUE, tc.update_time=CURRENT_TIMESTAMP 
                             WHERE project_id = :pid AND tc.user_id = :mid;"""), pid=pid, mid=mid)
        return True
    except:
        traceback.print_exc()
        return False
