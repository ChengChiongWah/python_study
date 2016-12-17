from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import Recipe, Material, Step


recipe = Blueprint('recipe', __name__, static_folder='../static' )
uploads_dir = 'static/images/'


def upload(f):
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        return path


def material_add(form, recipe_id):
    dic = {}
    for i in range(1, 11): #暂定用十种材料
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount' + str(i))
        if material_name:
            dic[material_name] = amount_value
    for k, v in dic.items():
        material = Material(k, v, recipe_id)
        material.add()

def material_update(form, recipe_id):
    material = Material.query.filter_by(recipe_id=recipe_id).first()
    for i in range(1, 11):
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount'+str(i))
        if material_name:
            material.update(material_name, amount_value)


def steps_add(form, recipe_id):
    for i in range(1, 11): #暂定只用十步
        step_number = i
        technique = form.get('step' + str(i) +'_introduce')
        f = request.files.get('step' + str(i) + '_pictures')
        if technique:
            picture_path = upload(f)
            steps = Step(i, technique, picture_path, recipe_id)
            steps.add()


def steps_update(form, recipe_id):
    steps = Step.query.filter_by(recipe_id=recipe_id).first()
    for i in range(1, 11):
        step_number = i
        technique = form.get('step' + str(i) + '_introduce')
        f = request.files.get('step' + str(i) + '_pictures')
        if technique:
            picture_path = upload(f)
            steps.update(step_number, technique, picture_path)



@recipe.route('/', methods=['GET'])
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
def recipe_add():
    form = request.form
    f = request.files.get('pictures')
    tips = form.get('tips')
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
        recipe = Recipe(form, path, tips)
        recipe.add()
        recipe_id = recipe.id
        material_add(form, recipe_id)
        steps_add(form, recipe_id)
    return redirect(url_for('main.index'))


@recipe.route('/recipe_information', methods=['GET'])
def recipe_information():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('recipe_information.html', recipes=recipes)


@recipe.route('/recipe_edit', methods=['GET'])
def recipe_edit():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    material_length = len(recipes.materials.all())
    return render_template('recipe_edit.html', recipes=recipes, material_length=material_length)


@recipe.route('/recipe_update', methods=['POST'])
def recipe_update():
    recipe_id = int(request.args.get('recipe_id'))
    form = request.form
    f = request.files.get('pictures')
    if f:
        filename = f.filename
        path = uploads_dir + filename
        f.save(path)
    else:
        path = ''
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    recipes.update(form, path)
    material_update(form, recipe_id)
    steps_update(form, recipe_id)
    return redirect(url_for('recipe.recipe_information', recipe_id=recipe_id))


@recipe.route('/recipe_delete', methods=['GET'])
def recipe_delete():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).all()
    materials = Material.query.filter_by(recipe_id=recipe_id)
    steps = Step.query.filter_by(recipe_id=recipe_id)
    for r in recipes:
        r.delete_element()
    for m in materials:
        m.delete_element()
    for s in steps:
        s.delete_element()
    return render_template(url_for('main.index'))