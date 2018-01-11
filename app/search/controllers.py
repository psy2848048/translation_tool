from flask import request, make_response, json
import app.search.models as model

def search():
    query = request.values.get('q', None)
    target_lang = request.values.get('tl', None)
    target = request.values.get('target', None)

    targets = target.split(',')
    results = {}

    for t in targets:
        #: 문장저장소 검색
        if t == 'tm':
            temp = []
            res = model.select_similarity_trans_memory(query, target_lang)
            for r in res:
                if r.score >= 50:
                    temp.append(dict(r))
            results['tm'] = temp

        #: 단어저장소 검색
        elif t == 'tb':
            res = model.select_termbase(query)
            results['tb'] = res

        #: 프로젝트 검색
        elif t == 'p':
            res = model.select_projects(query)
            results['p'] = res

        #: 문서 검색
        elif t == 'd':
            res = model.select_docs(query)
            results['d'] = res

        #: 사용자 검색
        elif t == 'u':
            res = model.select_users(query)
            results['u'] = res

    return make_response(json.jsonify(results), 200)
