from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for


recipe = Blueprint('recipe', __name__)

@recipe.route('/', methods=['GET'])
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
def recipe_add():
    pass