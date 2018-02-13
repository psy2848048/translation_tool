from app import db
from sqlalchemy import text
import re


def select_similarity_trans_memory(tid, query, origin_lang, trans_lang):
    conn = db.engine.connect()

    #: like에 넣을 부분 만들기 - 맨앞, 맨뒤 세음절
    split_sentence = query.split()
    first = "%" + ' '.join(split_sentence[:3]) + "%"
    second = "%" + ' '.join(split_sentence[-3:]) + "%"

    res = conn.execute(
        text("""SELECT longest_common_substring_percent(:sentence, sm.origin_text) as score
                     , tm_id, sm.origin_text, sm.trans_text
                     , username, user_id
                FROM (SELECT tm.id as tm_id, origin_text, trans_text 
                            , username, tm.user_id
                      FROM `marocat v1.1`.translation_memory tm 
                      JOIN (SELECT user_id, u.name as username
                            FROM `marocat v1.1`.project_members pm 
                            JOIN users u ON ( u.id = pm.user_id )
                            WHERE project_id=:pid AND u.is_deleted=FALSE AND pm.is_deleted=FALSE
                      ) t1 ON ( t1.user_id = tm.user_id )
                      WHERE ( origin_text LIKE :first OR origin_text LIKE :second )
                      AND origin_lang=:ol AND trans_lang=:tl AND tm.is_deleted = FALSE
                ) sm
                GROUP BY username, sm.trans_text
                ORDER BY score DESC 
                LIMIT 3;""")
        , sentence=query, first=first, second=second, ol=origin_lang, tl=trans_lang, pid=tid).fetchall()

    results = [dict(r) for r in res if r['score'] > 50]
    return results


def select_termbase(tid, query, origin_lang, trans_lang):
    conn = db.engine.connect()

    #: 검색 대상(query)의 마지막이 특수문자라면 지우기
    p = re.compile('[-=.#/?:$}]')
    m = p.match(query[-1])
    if m:
        nouns = query[:-1].split()
    else:
        nouns = query.split()

    temp = []
    for noun in nouns:
        # 추후 수정사항: 나중에 검색대상 구분하자
        if len(noun) > 2:
            res = conn.execute(
                text("""SELECT tb.id as term_id, origin_text, trans_text
                             , username, tb.user_id
                        FROM `marocat v1.1`.termbase tb 
                        JOIN (SELECT user_id, u.name as username
                            FROM `marocat v1.1`.project_members pm 
                            JOIN users u ON ( u.id = pm.user_id )
                            WHERE project_id=:pid AND u.is_deleted=FALSE AND pm.is_deleted=FALSE
                        ) t1 ON ( t1.user_id = tb.user_id )
                        WHERE origin_text LIKE :noun 
                        AND origin_lang = :ol AND trans_lang = :tl AND tb.is_deleted = FALSE 
                        GROUP BY username, trans_text;""")
                , noun='%'+noun+'%', ol=origin_lang, tl=trans_lang, pid=tid).fetchall()
        else:
            continue

        temp += [dict(r) for r in res]

    #: 중복되는 단어 제거하기
    terms = {frozenset(item.items()): item for item in temp}.values()
    return list(terms)


def select_projects(uid, query):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id as project_id, name, due_date, p.create_time 
                              FROM `marocat v1.1`.projects p JOIN project_members pm ON pm.project_id=p.id
                              WHERE name LIKE :query AND pm.user_id=:uid
                              AND p.is_deleted=FALSE AND pm.is_deleted=FALSE ;"""),
                       query='%' + query + '%', uid=uid)
    results = [dict(r) for r in res]
    return results


def select_docs(uid, query):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id as doc_id, title, origin_lang, trans_lang, due_date, d.create_time 
                              FROM `marocat v1.1`.docs d JOIN doc_members dm ON dm.doc_id=d.id
                              WHERE title LIKE :query AND dm.user_id=:uid
                              AND d.is_deleted=FALSE AND dm.is_deleted=FALSE ;"""),
                       query='%' + query + '%', uid=uid)
    results = [dict(r) for r in res]
    return results


def select_users(query):
    conn = db.engine.connect()

    res = conn.execute(text("""SELECT id as user_id, name, email FROM `marocat v1.1`.users
                               WHERE email=:query AND is_deleted=FALSE"""),
                       query=query).fetchall()
    results = [dict(r) for r in res]
    return results
