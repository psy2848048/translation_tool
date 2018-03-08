from flask import request, make_response, jsonify
import app.steem.models as model
from app import common, app
from datetime import datetime

from steem import Steem
from steem.post import Post
s = Steem(keys=app.config['STEEM_POSTING_KEY'])


def request_trans():
    post_url = request.form.get('post_url', None),
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    posting_key = request.form.get('posting_key', None)
    email = request.form.get('email', None)
    memo = request.form.get('memo', None)

    if None in [post_url, origin_lang, trans_lang]:
        return make_response(jsonify(result='Something Not Entered'), 460)

    permlink = '@{}'.format(post_url.split('@', maxsplit=1)[-1])
    #: 포스트 가져오기
    post = Post(post=permlink).export()
    name = post['author']
    content = common.convert_md2text(post['body'])

    #: 가격 측정하기
    price = model.set_price(content)

    #: 거래번호 만들기
    transaction_id = common.create_token(post_url, 20)

    #: 데이터베이스에 번역 의뢰 저장하기
    is_done = model.insert_trans_request(post_url, origin_lang, trans_lang, posting_key, content, email, name, price, memo, transaction_id)
    if is_done is False:
        return make_response(jsonify(result='Something Wrong'), 461)

    #: 견적 댓글 작성하기
    s.commit.post(title='의뢰하신 포스트의 번역 견적입니다',
                  body="""## `{name}`님이 의뢰하신 번역 견적서입니다\n
                  |       의뢰시간        |  언어   |  금액  |       거래번호       |
                  | :-------------------: | :-----: | :----: | :------------------: |
                  | {request_time} | {origin_lang} > {trans_lang} | $ {price} | {transaction_id} |
                  \n
                  > - 최종 공급가액에는 번역 및 초벌감수까지 포함되어 있습니다.
                  > -  번역물 제공 후 과하지 않은 선에서 추가 문의 및 검수 요청은 가능합니다.""".format(name=name, request_time=datetime.now(),
                                                                           origin_lang=origin_lang, trans_lang=trans_lang,
                                                                           price=price, transaction_id=transaction_id),
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

    return make_response(jsonify(result='OK'), 200)

