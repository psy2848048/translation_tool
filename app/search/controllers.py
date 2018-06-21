from flask import request, make_response, json
from flask_login import login_required, current_user
import app.search.models as model


@login_required
def search():
    uid = current_user.idx
    query = request.values.get('q', None)
    origin_lang = request.values.get('ol', None)
    trans_lang = request.values.get('tl', None)

    tid = request.values.get('tid', None)
    target = request.values.get('target', None)
    targets = target.split(',')

    results = {}
    for t in targets:
        #: 문장저장소 유사도 검색
        if t == 'tmS':
            # res = model.select_similarity_trans_memory(tid, query, origin_lang, trans_lang)
            res = model.select_similarity_trans_memory(query, origin_lang, trans_lang)
            results['tmS'] = res

        #: 문장저장소 일치 검색
        if t == 'tmE':
            res = model.select_exact_trans_memory(query)
            results['tmE'] = res

        #: 단어저장소 검색
        elif t == 'tb':
            if origin_lang.upper() == 'KO':
                res = model.select_termbase_in_ko(query, origin_lang, trans_lang)
                # res = model.select_termbase_in_ko(query, origin_lang, trans_lang)
            else:
                # res = model.select_en_termbase(tid, query, origin_lang, trans_lang)
                res = model.select_termbase_in_en(query, origin_lang, trans_lang)
            results['tb'] = res

        #: 프로젝트 검색
        elif t == 'p':
            res = model.select_projects(uid, query)
            results['p'] = res

        #: 문서 검색
        elif t == 'd':
            res = model.select_docs(uid, query)
            results['d'] = res

        #: 사용자 검색
        elif t == 'u':
            res = model.select_users(query)
            results['u'] = res

    return make_response(json.jsonify(results), 200)
