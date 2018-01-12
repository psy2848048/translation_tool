from flask import Blueprint
import app.search.controllers as ctrl

search = Blueprint('search', __name__)

search.add_url_rule('/', view_func=ctrl.search, methods=['POST'])
