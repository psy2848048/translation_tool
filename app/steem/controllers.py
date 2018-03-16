from flask import request, make_response, jsonify
import app.steem.models as model


def request_trans():
    post_url = request.form.get('postUrl', None),
    origin_lang = request.form.get('ol', None)
    trans_lang = request.form.get('tl', None)
    posting_key = request.form.get('postingKey', None)
    email = request.form.get('email', None)
    memo = request.form.get('memo', None)

    if None in [post_url, origin_lang, trans_lang]:
        return make_response(jsonify(result='Something Not Entered'), 460)

    is_done = model.insert_trans_request(post_url, origin_lang, trans_lang, posting_key, email, memo)

    if is_done is True:
        return make_response(jsonify(result='OK'), 200)
    else:
        return make_response(jsonify(result='Something Wrong'), 461)
