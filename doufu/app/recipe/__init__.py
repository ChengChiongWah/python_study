from flask import Blueprint

recipe = Blueprint('recipe', __name__, static_folder='../static')

from . import views

