from flask import request, make_response, json
from flask_login import login_required, current_user
import app.search.models as model


@login_required
def search():
    uid = current_user.idx
    query = request.values.get('q', None)
    origin_lang = request.values.get('ol', None)
    trans_lang = request.values.get('tl', None)

    target = request.values.get('target', None)
    targets = target.split(',')

    results = {}
    for t in targets:
        #: 문장저장소 검색
        if t == 'tm':
            temp = []
            res = model.select_similarity_trans_memory(uid, query, origin_lang, trans_lang)
            results['tm'] = res

        #: 단어저장소 검색
        elif t == 'tb':
            res = model.select_termbase(uid, query, origin_lang, trans_lang)
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
