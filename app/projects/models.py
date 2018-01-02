from app import db
from sqlalchemy import Table, MetaData, text

def select_projects(user_id):
    conn = db.engine.connect()

    #: 추후 수정 예정 - progress_percent가 DECIMAL 문제로 계속 0으로 출력된다.
    projects = conn.execute(text("""SELECT p.id as project_id, p.name as project_name, p.status, p.create_time, p.duration_date,
                                                   progress_percent, 
                                                   c.name as client_company, group_concat(u.username) as clients
                                    FROM marocat.projects p JOIN ( SELECT projects_id, user_id FROM marocat.project_members WHERE user_id = :user_id) t1 ON ( p.id = t1.projects_id) 
                                                            JOIN ( SELECT pd.projects_id as pid, 
                                                                          CAST(FLOOR(SUM(ds.status) / COUNT(*) * 100) AS CHAR) as progress_percent 
                                                                   FROM marocat.doc_sentences ds JOIN marocat.project_docs pd ON ( pd.id = ds.project_docs_id ) 
                                                                   GROUP BY pd.projects_id) t2 ON ( p.id = t2.pid )
                                                            JOIN ( marocat.project_members pm, marocat.users u, marocat.company c ) ON ( p.id = pm.projects_id AND pm.user_id = u.id AND u.company_id = c.id )
                                    WHERE u.usertype = 'C'
                                    GROUP BY p.id;"""), user_id=user_id)
    return projects

def select_project_info(project_id):
    conn = db.engine.connect()
    results = conn.execute(text(""" SELECT p.id, p.name, p.status, p.create_time, p.duration_date,
                                           trans_company, translators,
                                           client_company, clients,
                                           origin_langs, trans_langs
                                    FROM marocat.projects p JOIN ( SELECT pm.projects_id as pid, c.name as trans_company, group_concat( DISTINCT u.username) as translators
                                                                                          FROM marocat.project_members pm JOIN ( marocat.users u, marocat.company c ) ON ( pm.user_id = u.id AND u.company_id = c.id )
                                                                                          WHERE usertype = 'T' AND pm.projects_id = :project_id ) t1 ON ( t1.pid = p.id )
                                                                              JOIN ( SELECT pm.projects_id as pid, c.name as client_company, group_concat( DISTINCT u.username) as clients
                                                                                          FROM marocat.project_members pm JOIN ( marocat.users u, marocat.company c ) ON ( pm.user_id = u.id AND u.company_id = c.id )
                                                                                          WHERE usertype = 'C' AND pm.projects_id = :project_id ) t2 ON ( t2.pid = p.id )
                                                                              JOIN ( SELECT projects_id as pid, group_concat( DISTINCT origin_lang) as origin_langs, group_concat( DISTINCT trans_lang) as trans_langs
                                                                                          FROM marocat.project_docs GROUP BY projects_id ) t3 ON ( t3.pid = p.id )
                                    WHERE p.id = :project_id;"""), project_id=project_id)
    return results

def select_project_docs_list(project_id):
    conn = db.engine.connect()
    results = conn.execute(text(""" SELECT pd.id as project_docs_id, title, pd.status, link, trans_lang, duration_date,
                                           progress_percent,
                                           c.name as trans_company, group_concat(u.username) as translators
                                    FROM marocat.project_docs pd JOIN ( SELECT project_docs_id as pdid, CAST(FLOOR(SUM(status) / COUNT(*) * 100) AS CHAR) as progress_percent
                                                                        FROM marocat.doc_sentences
                                                                        GROUP BY project_docs_id ) t1 ON ( t1.pdid = pd.id )
                                                                 LEFT OUTER JOIN ( marocat.project_members pm, marocat.users u, marocat.company c ) ON ( pd.id = pm.project_docs_id AND pm.user_id = u.id AND u.company_id = c.id )
                                    WHERE pd.projects_id = :project_id
                                    GROUP BY pd.id;"""), project_id=project_id)
    return results