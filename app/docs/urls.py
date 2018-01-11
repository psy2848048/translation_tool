from flask import Blueprint
import app.docs.controllers as ctrl

docs = Blueprint('docs', __name__)

docs.add_url_rule('/<int:did>', view_func=ctrl.get_doc_info, methods=['GET'])
docs.add_url_rule('/<int:did>/members', view_func=ctrl.get_doc_members, methods=['GET'])

docs.add_url_rule('/<int:did>', view_func=ctrl.modify_doc_info, methods=['PUT'])
docs.add_url_rule('/<int:did>/members/<int:mid>/permission', view_func=ctrl.modify_doc_member, methods=['PUT'])

docs.add_url_rule('/<int:did>', view_func=ctrl.delete_doc, methods=['DELETE'])
