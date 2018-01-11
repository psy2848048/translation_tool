from flask import Blueprint
import app.trans_memory.controllers as ctrl

trans_memory = Blueprint('trans_memory', __name__)

trans_memory.add_url_rule('/', view_func=ctrl.get_trans_memory_list, methods=['GET'])
trans_memory.add_url_rule('/', view_func=ctrl.save_trans_memory, methods=['POST'])
trans_memory.add_url_rule('/<int:tid>', view_func=ctrl.modify_trans_memory, methods=['PUT'])