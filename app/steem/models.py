from app import app, db, common
from sqlalchemy import MetaData, Table
import traceback
import re
from markdown import markdown
from bs4 import BeautifulSoup as BS
from datetime import datetime

from steem import Steem
from steem.post import Post
s = Steem(keys=app.config['STEEM_POSTING_KEY'])


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


def insert_trans_request(link, origin_lang, trans_lang, posting_key, email, memo):
    conn = db.engine.connect()
    trans = conn.begin()
    meta = MetaData(bind=db.engine)
    t1 = Table('request', meta, autoload=True)
    t2 = Table('token', meta, autoload=True)

    #: 포스트 가져오기
    permlink = '@{}'.format(link.split('@', maxsplit=1)[-1])
    post = Post(post=permlink).export()
    name = post['author']

    #: 포스트 마크다운 형식 지우고 내용만 뽑아내기
    html = markdown(post['body'])
    soup = BS(html, 'lxml')
    content = ''.join(soup.find_all(text=True))

    #: 가격 측정하기
    price = set_price(content)

    #: 거래번호 만들기
    transaction_id = common.create_token(link, 20)

    #: 데이터베이스에 저장하기
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
    except:
        traceback.print_exc()
        trans.rollback()
        return False

    #: 견적 댓글 등록하기
    title = '의뢰하신 포스트의 번역 견적입니다'
    comment = """
    ## `{name}`님이 의뢰하신 번역 견적서입니다
    | 의뢰시간   | 언어    | 금액  | 거래번호      |
    | :--------: | :-----: | :---: | :-----------: |
    | {request_time} | {origin_lang} > {trans_lang} | $ {price} | {transaction_id} |
    > - 최초 공급가액에는 번역 및 초벌감수까지 포함되어 있습니다.
    > - 번역물 제공 후 과하지 않은 선에서 추가 문의 및 검수 요청은 가능합니다.
    """.format(name=name, request_time=datetime.now(), origin_lang=origin_lang, trans_lang=trans_lang,
               price=price, transaction_id=transaction_id)

    is_done = write_comment(permlink, title, comment)
    if is_done is True:
        return True
    else:
        return False


def write_comment(permlink, title, comment):
    try:
        s.commit.post(title=title,
                      body=comment,
                      author='ciceron',
                      permlink=None,  # Manually set the permlink (defaults to None). If left empty, it will be derived from title automatically
                      reply_identifier=permlink,  # Identifier of the parent post/comment (only if this post is a reply/comment) (eg. @author/permlink)
                      json_metadata=None,
                      comment_options=None,
                      # comment_options = {
                      #     'max_accepted_payout': '1000000.000 SBD',
                      #     'percent_steem_dollars': 10000,
                      #     'allow_votes': True,
                      #     'allow_curation_rewards': True,
                      #     'extensions': [
                      #         [0,
                      #          {
                      #              'beneficiaries': [
                      #                  {'account': 'account1', 'weight': 5000},
                      #                  {'account': 'account2', 'weight': 5000},
                      #              ]
                      #          }
                      #         ]
                      #     ]
                      # },
                      community=None,
                      tags=None,  # (str, list)
                                  # (Optional) A list of tags (5 max) to go with the post. This will also override the tags specified in json_metadata.
                                  # The first tag will be used as a ‘category’. If provided as a string, it should be space separated.
                      beneficiaries=None,
                      self_vote=False)
        return True
    except:
        traceback.print_exc()
        return False


def get_post_content(link):
    permlink = '@{}'.format(link.split('@', maxsplit=1)[-1])
    post = Post(post=permlink).export()
    return post
