from flask import Blueprint
import app.workbench.controllers as ctrl

workbench = Blueprint('workbench', __name__)

workbench.add_url_rule('/docs/<int:did>', view_func=ctrl.get_doc, methods=['GET'])

workbench.add_url_rule('/docs/origins/<int:oid>/trans', view_func=ctrl.save_new_trans_sentence, methods=['POST'])
workbench.add_url_rule('/docs/trans/<int:tid>', view_func=ctrl.modify_trans_sentence, methods=['PUT'])
workbench.add_url_rule('/docs/trans/<int:tid>/status/<int:status>', view_func=ctrl.update_trans_status, methods=['PUT'])

workbench.add_url_rule('/docs/trans/<int:tid>/comments', view_func=ctrl.get_trans_comments, methods=['GET'])
workbench.add_url_rule('/docs/trans/<int:tid>/comments', view_func=ctrl.make_trans_comment, methods=['POST'])
workbench.add_url_rule('/docs/trans/<int:tid>/comments/<int:cid>', view_func=ctrl.delete_trans_comment, methods=['DELETE'])
