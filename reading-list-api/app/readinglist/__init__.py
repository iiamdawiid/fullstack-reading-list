from flask import Blueprint

reading_list_blueprint = Blueprint('reading_list', __name__, url_prefix='/reading_list')

from . import routes