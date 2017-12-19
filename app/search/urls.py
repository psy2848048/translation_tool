from flask import Blueprint
import app.search.controllers as ctrl

search = Blueprint('search', __name__)

# search.add_url_rule('/', view_func=ctrl.index, methods=['GET'])
# search.add_url_rule('/<string:search_type>', view_func=ctrl.search, methods=['GET'])

search.add_url_rule('/word', view_func=ctrl.search_word, methods=['GET'])
