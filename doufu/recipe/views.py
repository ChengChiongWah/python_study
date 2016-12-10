from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import Recipe, Material, Steps


recipe = Blueprint('recipe', __name__)
uploads_dir = 'static/images/'

def upload(f):
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        return path


def material_add(form, recipe_name):
    dic = {}
    for i in range(1, 11): #暂定用十种材料
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount' + str(i))
        if material_name:
            dic[material_name] = amount_value
    for k, v in dic.items():
        material = Material(k, v, recipe_name)
        material.add()

def steps_add(form, recipename):
    for i in range(1, 11): #暂定只用十步
        step_number = i
        technique = form.get('step' + str(i) +'_introduce')
        f = request.files.get('step' + str(i) + '_pictures')
        if technique:
            picture_path = upload(f)
            recipename = recipename
            steps = Steps(i, technique, picture_path, recipename)
            steps.add()

@recipe.route('/', methods=['GET'])
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
def recipe_add():
    form = request.form
    f = request.files.get('pictures')
    recipe_name = form.get('name')
    tips = form.get('tips')
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        recipe = Recipe(form, path, tips)
        recipe.add()
        material_add(form, recipe_name)
        steps_add(form, recipe_name)
    return redirect(url_for('main.index'))
