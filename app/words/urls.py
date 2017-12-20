from flask import Blueprint
import app.words.controllers as ctrl

words = Blueprint('words', __name__)

words.add_url_rule('/', view_func=ctrl.get_words, methods=['GET'])
words.add_url_rule('/files', view_func=ctrl.save_words_files, methods=['POST'])
words.add_url_rule('/', view_func=ctrl.save_word, methods=['POST'])
words.add_url_rule('/<int:word_id>', view_func=ctrl.modify_word, methods=['PUT'])
