from flask import Blueprint
import app.docs.controllers as ctrl

docs = Blueprint('docs', __name__)

docs.add_url_rule('/', view_func=ctrl.make_project_doc, methods=['POST'])
docs.add_url_rule('/<int:doc_id>', view_func=ctrl.get_doc_for_translate, methods=['GET'])
# docs.add_url_rule('/<int:doc_id>', view_func=ctrl.modify_doc, methods=['PUT'])
# docs.add_url_rule('/<int:doc_id>', view_func=ctrl.delete_doc, methods=['DELETE'])


###: sentences
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>', view_func=ctrl.get_translate_and_words, methods=['GET'])
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>', view_func=ctrl.save_translation, methods=['PUT'])
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>/status/<int:status>', view_func=ctrl.update_trans_status, methods=['PUT'])


###: commnets
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>/comments', view_func=ctrl.get_comments, methods=['GET'])
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>/comments', view_func=ctrl.make_comment, methods=['POST'])
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>/comments/<int:comment_id>', view_func=ctrl.modify_comment, methods=['PUT'])
docs.add_url_rule('/<int:doc_id>/sentences/<int:sentence_id>/comments/<int:comment_id>', view_func=ctrl.delete_comment, methods=['DELETE'])
