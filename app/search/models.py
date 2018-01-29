from app import db
from sqlalchemy import Table, MetaData
from sqlalchemy import text
import re


def select_similarity_trans_memory(query, origin_lang, trans_lang):
    conn = db.engine.connect()

    #: like에 넣을 부분 만들기 - 맨앞, 맨뒤 세음절
    split_sentence = query.split()
    first = "%" + ' '.join(split_sentence[:3]) + "%"
    second = "%" + ' '.join(split_sentence[-3:]) + "%"

    res = conn.execute(
        text("""SELECT longest_common_substring_percent(:sentence, sm.origin_text) as score
                     , tm_id, sm.origin_text, sm.trans_text
                     , username, user_id
                FROM ( SELECT tm.id as tm_id, origin_text, trans_text 
                            , u.name as username, u.id as user_id
                        FROM `marocat v1.1`.translation_memory tm 
                        JOIN ( users_tmlist ut, users u ) 
                        ON ( ut.tm_id = tm.id AND u.id = ut.user_id AND ut.is_deleted = FALSE AND u.is_deleted = FALSE )
                        WHERE ( origin_text LIKE :first OR origin_text LIKE :second )
                        AND origin_lang = :ol AND trans_lang = :tl AND tm.is_deleted = FALSE) sm
                GROUP BY username
                ORDER BY score DESC 
                LIMIT 3;""")
        , sentence=query, first=first, second=second, ol=origin_lang, tl=trans_lang).fetchall()

    results = [dict(r) for r in res]
    return results


def select_termbase(query, origin_lang, trans_lang):
    conn = db.engine.connect()
    nouns = query[:-1].split()
    print(nouns)

    temp = []
    for noun in nouns:
        # 추후 수정사항: 나중에 검색대상 구분하자
        if len(noun) > 2:
            res = conn.execute(
                text("""SELECT tb.id as term_id, origin_text, trans_text, u.name as username, u.id as user_id
                        FROM `marocat v1.1`.termbase tb 
                        JOIN ( users_tblist ut, users u ) 
                        ON ( ut.tb_id = tb.id AND u.id = ut.user_id AND ut.is_deleted = FALSE AND u.is_deleted = FALSE )
                        WHERE origin_text LIKE :noun 
                        AND origin_lang = :ol AND trans_lang = :tl AND tb.is_deleted = FALSE 
                        GROUP BY u.name, trans_text;""")
                , noun='%'+noun+'%', ol=origin_lang, tl=trans_lang).fetchall()
        else:
            continue

        temp += [dict(r) for r in res]

    #: 중복되는 단어 제거하기
    terms = {frozenset(item.items()): item for item in temp}.values()
    return list(terms)


def select_termbase_only_one(query):
    """
    유사한 단어 없이, 완전히 query와 일치하는 단어 찾는다.
    :param query:
    :return:
    """
    conn = db.engine.connect()
    words = []

    res = conn.execute(text("""SELECT id as term_id, trans_lang, origin_text, trans_text FROM marocat.word_memory 
                               WHERE is_deleted = FALSE AND (origin_text LIKE :noun OR trans_text LIKE :noun );"""), noun='%'+query+'%')

    temp = {}
    for r in res:
        if r.trans_lang is not 'ko':
            temp['term_id'] = r.term_id
            temp['origin_text'] = r.origin_text
            temp['trans_text'] = r.trans_text
            words.append(temp)
        else:
            temp['term_id'] = r.term_id
            temp['origin_text'] = r.trans_text
            temp['trans_text'] = r.origin_text
            words.append(temp)
    return words


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
                               WHERE email = :query"""),
                       query=query)
    results = [dict(r) for r in res]
    return results
