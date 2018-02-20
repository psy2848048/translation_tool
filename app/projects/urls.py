from flask import Blueprint
import app.projects.controllers as ctrl

projects = Blueprint('projects', __name__)

projects.add_url_rule('/', view_func=ctrl.get_projects_list, methods=['GET'])
projects.add_url_rule('/<int:pid>', view_func=ctrl.get_project_info, methods=['GET'])
projects.add_url_rule('/<int:pid>/docs', view_func=ctrl.get_proejct_docs, methods=['GET'])
projects.add_url_rule('/<int:pid>/members', view_func=ctrl.get_proejct_members, methods=['GET'])

projects.add_url_rule('/', view_func=ctrl.add_project, methods=['POST'])
projects.add_url_rule('/<int:pid>/docs', view_func=ctrl.add_doc, methods=['POST'])
projects.add_url_rule('/<int:pid>/members', view_func=ctrl.add_project_member, methods=['POST'])

projects.add_url_rule('/<int:pid>', view_func=ctrl.modify_project_info, methods=['PUT'])
projects.add_url_rule('/<int:pid>/members/<int:mid>/permission', view_func=ctrl.modify_project_member, methods=['PUT'])

projects.add_url_rule('/<int:pid>', view_func=ctrl.delete_project, methods=['DELETE'])
projects.add_url_rule('/<int:pid>/members/<int:mid>', view_func=ctrl.delete_project_member, methods=['DELETE'])
