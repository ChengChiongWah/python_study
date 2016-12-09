from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import Recipe, Material


recipe = Blueprint('recipe', __name__)
uploads_dir = 'static/images/'

def upload(f):
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        return path


def material_add(form):
    dic = {}
    for i in range(1, 11):
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount' + str(i))
        if material_name:
            dic[material_name] = amount_value
    return dic


@recipe.route('/', methods=['GET'])
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
def recipe_add():
    form = request.form
    f = request.files.get('pictures')
    recipe_name = form.get('name')
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        recipe = Recipe(form, path)
        recipe.add()
    dic = material_add(form)
    for k, v in dic.items():
        material = Material(k, v, recipe_name)
        material.add()
    return redirect(url_for('main.index'))
