from flask import Blueprint
import app.steem.controllers as ctrl

steem = Blueprint('steem', __name__)

steem.add_url_rule('/transRequest', view_func=ctrl.request_trans, methods=['POST'])
