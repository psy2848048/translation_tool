from flask import Blueprint
import app.comments.controllers as ctrl

comments = Blueprint('comments', __name__)

comments.add_url_rule('/', view_func=ctrl.get_comments, methods=['GET'])
comments.add_url_rule('/', view_func=ctrl.make_comment, methods=['POST'])
comments.add_url_rule('/<int:comment_id>', view_func=ctrl.modify_comment, methods=['PUT'])
comments.add_url_rule('/<int:comment_id>', view_func=ctrl.delete_comment, methods=['DELTE'])
