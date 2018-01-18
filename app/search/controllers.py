from flask import request, make_response, json, session
from flask_login import login_required, current_user
import app.search.models as model

def search():
    # uid = current_user.id
    uid = 7
    query = request.values.get('q', None)
    origin_lang = request.values.get('ol', None)
    target = request.values.get('target', None)

    targets = target.split(',')
    results = {}

    for t in targets:
        #: 문장저장소 검색
        if t == 'tm':
            temp = []
            res = model.select_similarity_trans_memory(query)
            for r in res:
                if r.score >= 50:
                    temp.append(dict(r))
            results['tm'] = temp

        #: 단어저장소 검색
        elif t == 'tb':
            res = model.select_termbase(query, origin_lang)
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
