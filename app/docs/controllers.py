from flask import request, make_response, json
import app.docs.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Docs API', user_id=user_id), 200)

def make_project_doc(user_id):
    title = request.form.get('title', None)
    doc = request.form.get('doc', None)
    link = request.form.get('link', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    trans_company = request.form.get('trans_company', None)
    translators = request.form.get('translators', None)
    translator = request.form.get('translator', None)
    duration_time = request.form.get('duration_time', None)
    # file = request.files.get('file', None)

    return make_response(json.jsonify(result=''), 200)

def get_doc_for_translate(user_id, doc_id):
    result = []
    doc_sentences = model.select_doc_sentences(doc_id)

    for ds in doc_sentences:
        # print(ds.id, ds.origin_text, ds.trans_text)
        result.append(dict(ds))

    return make_response(json.jsonify(result=result), 200)

def modify_doc(user_id, doc_id):
    return make_response(json.jsonify(result=''), 200)

def delete_doc(user_id, doc_id):
    return make_response(json.jsonify(result=''), 200)



##################################   sentences   ##################################

def get_translate_and_words(user_id, doc_id, sentence_id):
    origin_text = request.form.get('origin_text', None)

    if not origin_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    similarity_res = model.get_similarity_sentences()
    words = model.search_words_in_sentence()

    return make_response(json.jsonify(tm=similarity_res, words=words), 200)

def save_translation(user_id, doc_id, sentence_id):
    trans_type = request.values.get('trans_type', None)
    trans_text = request.values.get('trans_text', None)

    is_done = model.update_trans_text_and_type(sentence_id, trans_text, trans_type)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def update_trans_status(user_id, doc_id, sentence_id, status):
    is_done = model.update_trans_status(sentence_id, status)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)



##################################   comments   ##################################

def get_comments(user_id, doc_id, sentence_id):
    results = []

    comments = model.select_sentence_comments(doc_id, sentence_id)
    for c in comments:
        results.append(dict(c))

    return make_response(json.jsonify(result=results), 200)

def make_comment(user_id, doc_id, sentence_id):
    comment = request.form.get('comment', None)

    if not doc_id or not sentence_id or not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_sentence_comment(user_id, doc_id, sentence_id, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_comment(user_id, doc_id, sentence_id, comment_id):
    comment = request.form.get('comment', None)

    if not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.update_sentence_comment(comment_id, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def delete_comment(user_id, doc_id, sentence_id, comment_id):
    is_done = model.delete_sentence_comment(comment_id)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)