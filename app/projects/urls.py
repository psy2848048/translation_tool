from flask import Blueprint
import app.projects.controllers as ctrl

projects = Blueprint('projects', __name__)

projects.add_url_rule('/', view_func=ctrl.get_projects_list, methods=['GET'])
projects.add_url_rule('/', view_func=ctrl.make_project, methods=['POST'])
# projects.add_url_rule('/', view_func=ctrl.modify_project, methods=['PUT'])
# projects.add_url_rule('/', view_func=ctrl.delete_project, methods=['DELETE'])

projects.add_url_rule('/<int:project_id>', view_func=ctrl.get_project_info, methods=['GET'])
projects.add_url_rule('/<int:project_id>/docs', view_func=ctrl.get_proejct_docs_list, methods=['GET'])

projects.add_url_rule('/<int:project_id>/members', view_func=ctrl.get_project_members, methods=['GET'])
projects.add_url_rule('/<int:project_id>/members', view_func=ctrl.add_project_member, methods=['POST'])
# projects.add_url_rule('/<int:project_id>/members', view_func=ctrl.delete_project_members, methods=['DELETE'])

