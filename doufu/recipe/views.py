from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import Recipe


recipe = Blueprint('recipe', __name__)
uploads_dir = 'static/images/'

@recipe.route('/', methods=['GET'])
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
def recipe_add():
    form = request.form
    f = request.files.get('pictures')
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
    recipe = Recipe(form, path)
    recipe.add()
    return redirect(url_for('main.index'))
