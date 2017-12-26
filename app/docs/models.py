from app import db
from sqlalchemy import Table, MetaData
from sqlalchemy import text
import traceback
import datetime
import re
import nltk

def select_doc_sentences(doc_id):
    conn = db.engine.connect()
    doc_sentences = conn.execute('select id as sentence_id, project_docs_id as doc_id, origin_text, trans_text, status, trans_type from marocat.doc_sentences where project_docs_id = {} and is_deleted = FALSE;'.format(doc_id))

    # meta = MetaData(bind=db.engine)
    # ds = Table('doc_sentences', meta, autoload=True)
    # doc_sentences = ds.select(ds.c.project_docs_id == doc_id and ds.c.is_deleted == False).execute()

    return doc_sentences



##################################   sentences   ##################################

# from ckonlpy.tag import Twitter
# twit = Twitter()
# def ko_devide_by_morpheme(sentence):
#     t1 = re.sub(r"[(]\w+[)]", '', sentence)
#     t2 = re.findall(r'\w+', re.sub(r'\d+', '', t1))
#     texts = [twit.pos(t)[0][0] for t in t2]
#     texts.append(''); texts.insert(0, '')
#     return texts
#
# def ko_devide_by_spacing(self, sentence):
#     t1 = re.sub(r"[(]\w+[)]", '', sentence)
#     t2 = re.findall(r'\w+', t1)  # ['나는', '18일에', '철수와', '밥을', '먹었다']
#     texts = [t for t in t2 if re.match(r'\D+', t) is not None]  # ['나는', '철수와', '밥을', '먹었다']
#     # texts.append('')  # ['얼마나', '오래', '비가', '내렸습니까', '']
#     # texts.insert(0, '')  # ['', '얼마나', '오래', '비가', '내렸습니까', '']
#     return texts
#
# def get_morphemes_of_en_sentence(sentence):
#     nouns = []
#     t = nltk.word_tokenize(sentence)
#     tt = nltk.pos_tag(t)
#
#     for word, tag in tt:
#         if tag in ['FW', 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'RB', 'RBR', 'RBS', 'RP', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
#             nouns.append(word)
#
#     return nouns

def get_similarity_sentences(sentence):
    conn = db.engine.connect()

    #: like에 넣을 부분 만들기 - 맨앞, 맨뒤 세음절
    split_sentence = sentence.split()
    first = "%" + ' '.join(split_sentence[:3]) + "%"
    second = "%" + ' '.join(split_sentence[-3:]) + "%"

    search_sentence_memory = """SELECT longest_common_substring_percent(:sentence, sm.origin_text) as score, sm.origin_text, sm.trans_text
                                FROM ( SELECT origin_text, trans_text FROM marocat.sentence_memory
                                       WHERE origin_text LIKE :first OR origin_text LIKE :second ) sm
                                ORDER BY score DESC
                                LIMIT 3;"""
    similarity_sentences = conn.execute(text(search_sentence_memory), sentence=sentence, first=first, second=second)

    return similarity_sentences

def select_words_in_sentence(sentence):
    conn = db.engine.connect()
    temp_words = []
    nouns = sentence.split()

    for noun in nouns:
        res = conn.execute(text("""SELECT id as word_id, trans_lang, origin_text, trans_text FROM marocat.word_memory 
                                   WHERE is_deleted = FALSE AND (origin_text LIKE :noun OR trans_text LIKE :noun)
                                     AND (
                                        CHAR_LENGTH(origin_text) BETWEEN CHAR_LENGTH(:noun_pure) - 4 AND CHAR_LENGTH(:noun_pure) + 4
                                      -- OR
                                        -- CHAR_LENGTH(trans_text) BETWEEN CHAR_LENGTH(:noun_pure) - 4 AND CHAR_LENGTH(:noun_pure) + 4
                                   )"""), noun='%'+noun+'%', noun_pure=noun)

        temp = {}
        for r in res:
            if r.trans_lang is not 'ko':
                temp['word_id'] = r.word_id
                temp['origin_text'] = r.origin_text
                temp['trans_text'] = r.trans_text
                temp_words.append(temp
            else:
                temp['word_id'] = r.word_id
                temp['origin_text'] = r.trans_text
                temp['trans_text'] = r.origin_text
                temp_words.append(temp)

    #: 중복되는 단어 제거하기
    words = {frozenset(item.items()): item for item in temp_words}.values()

    return list(words)

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

