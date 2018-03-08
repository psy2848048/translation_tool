from app import db
from sqlalchemy import MetaData, Table
import traceback
import re


def set_price(content):
    """
    1. http~와 같은 링크와 특수문자를 삭제한다
    2. 스팀용 씨세론 번역비 계산법에 의하여 가격을 측정한다
    :param content: 포스트 내용
    :return: 금액
    """
    #: link 삭제하기
    t1 = re.sub(r'http\S+', '', content, flags=re.MULTILINE)

    #: 특수문자 삭제하기
    t2 = re.sub('\W', '', t1)

    #: 금액 계산하기
    price = len(t2) * 0.0001
    return price


def insert_trans_request(link, origin_lang, trans_lang, posting_key, content, email, name, price, memo, transaction_id):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    t1 = Table('request', meta, autoload=True)
    t2 = Table('token', meta, autoload=True)

    try:
        #: transaction_id 저장하기
        conn.execute(t2.insert(), token=transaction_id, issue_to=email, memo=name + '(' + email + ')에게 번역 거래번호 발급')

        #: 번역 의뢰 저장하기
        res = conn.execute(t1.insert(), origin_lang=origin_lang, trans_lang=trans_lang,
                           posting_key=posting_key, content=content, link=link, client_memo=memo,
                           client_email=email, client_name=name, price=price, transaction_id=transaction_id,
                           admin_email='contact@ciceron.me', status=1, request_from='steemit')

        if res.rowcount != 1:
            trans.rollback()
            return False

        trans.commit()
        return True
    except:
        traceback.print_exc()
        trans.rollback()
        return False

