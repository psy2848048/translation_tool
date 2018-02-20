from flask import Blueprint
import app.termbase.controllers as ctrl

termbase = Blueprint('termbase', __name__)

termbase.add_url_rule('/', view_func=ctrl.get_termbase_list, methods=['GET'])
termbase.add_url_rule('/', view_func=ctrl.save_termbase, methods=['POST'])
termbase.add_url_rule('/<int:tid>', view_func=ctrl.modify_term, methods=['PUT'])
termbase.add_url_rule('/<int:tid>', view_func=ctrl.delete_term, methods=['DELETE'])
