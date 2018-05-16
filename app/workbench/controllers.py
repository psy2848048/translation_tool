from flask import request, make_response, json
from flask_login import login_required, current_user
import app.workbench.models as model


@login_required
def get_doc(did):
    doc_sentences = model.select_doc(did)
    return make_response(json.jsonify(results=doc_sentences), 200)


@login_required
def get_trans_comments(did, sid):
    comments = model.select_trans_comments(sid)
    return make_response(json.jsonify(results=comments), 200)


# @login_required
def output_doc_to_file(did):
    output_type = request.values.get('type', None)

    if output_type is None:
        return make_response(json.jsonify('Something Not Entered'), 460)

    file, is_done = model.export_doc(output_type, did)

    if is_done is True:
        # return send_file(io.BytesIO(file[0]), attachment_filename=file[1])

        response = make_response(file[0])
        cd = 'attachment; filename={}'.format(file[1])
        response.headers['Content-Disposition'] = cd

        #: mimetype 설정
        if output_type == 'txt':
            response.mimetype = 'text/text'
        else:
            response.mimetype = 'text/{}'.format(output_type)
        return response
    else:
        return make_response(json.jsonify(result='Something Wrong'), 461)


@login_required
def save_trans_sentence(sid):
    trans_text = request.values.get('trans_text', None)
    trans_type = request.values.get('trans_type', None)

    is_done = model.insert_or_update_trans(sid, trans_text, trans_type)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def add_trans_comment(did, sid):
    uid = current_user.idx
    comment = request.form.get('comment', None)

    if not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_trans_comment(uid, did, sid, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_sentence_status(sid, status):
    is_done = model.update_sentence_status(sid, status)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def delete_trans_comment(cid):
    is_done = model.delete_trans_comment(cid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def get_doc_comments(did):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 50))

    comments, total_cnt = model.select_doc_comments(did, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=comments), 200)


@login_required
def add_doc_comment(did):
    uid = current_user.idx
    comment = request.form.get('comment', None)

    if not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_doc_comment(uid, did, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def delete_doc_comment(cid):
    uid = current_user.idx
    is_done = model.delete_trans_comment(cid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_origin_sentence(sid):
    uid = current_user.idx
    original_text = request.form.get('original_text', None)

    if not original_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done, updated_sid, updated_text = model.update_origin_sentence(uid, sid, original_text)

    if is_done is True:
        return make_response(json.jsonify(#modified_user_id=uid,
                                          sid=updated_sid, original_text=updated_text), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
