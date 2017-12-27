from sqlalchemy import Table, MetaData, text

from app import db

def basic():
    conn = db.engine.connect()
    meta = MetaData(bind=db.engine)

    projects = Table('projects', meta, autoload=True)
    conn.execute(projects.insert(), name='test')

    a = projects.select(projects.c.name == 'test').execute()
    for aa in a: print(aa)

    a = projects.select(projects.c.name == 'test').execute().first()
    print(a)

def select_projects(user_id):
    conn = db.engine.connect()
    projects = conn.execute(text("""SELECT p.id as project_id, p.name as project_name, progress_percent, p.status, c.name as client_company, group_concat(u.username) as clients, p.create_time, p.duration_date
FROM marocat.projects p JOIN ( SELECT projects_id, user_id FROM marocat.project_members WHERE user_id = :user_id ) t1 ON ( p.id = t1.projects_id) 
										  JOIN ( SELECT pd.projects_id as pid, CAST(FLOOR(SUM(ds.status) / COUNT(*) * 100) AS CHAR) as progress_percent FROM marocat.doc_sentences ds JOIN marocat.project_docs pd ON ( pd.id = ds.project_docs_id ) GROUP BY pd.projects_id) t2 ON ( p.id = t2.pid )
                                          JOIN ( marocat.project_members pm, marocat.users u, marocat.company c ) ON ( p.id = pm.projects_id AND pm.user_id = u.id AND u.company_id = c.id )
WHERE u.usertype = 'C'
GROUP BY p.id;"""), user_id=user_id)
    return projects