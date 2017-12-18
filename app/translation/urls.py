from flask import Blueprint
import app.translation.controllers as ctrl

translation = Blueprint('translation', __name__)

translation.add_url_rule('/<int:sentence_id>', view_func=ctrl.get_translate_and_words, methods=['GET'])
translation.add_url_rule('/<int:sentence_id>', view_func=ctrl.save_translation, methods=['PUT'])
translation.add_url_rule('/<int:sentence_id>/status/<int:status>', view_func=ctrl.save_translation_status, methods=['PUT'])
