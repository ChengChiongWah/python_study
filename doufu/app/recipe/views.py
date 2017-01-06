from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from werkzeug.utils import secure_filename
from flask_login import login_required
from . import recipe
from ..models import Material, Recipe, Step
from ..log import Log
import os

uploads_dir = 'static/images/'
allow_extensions = set(['png', 'jpg', 'jpeg']) #允许的图片格式


def allowed_file(filename):  #允许的文件格式
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allow_extensions


def upload(f, file_formate):
    if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        path = uploads_dir + filename
        f.save(path)
        if file_formate:
            os.rename(uploads_dir+filename, uploads_dir+file_formate+filename) # 按给定格式修改上传的文件
            filename = uploads_dir + file_formate + filename
            return filename
        else:
            return filename


def material_add(form, recipe_id):
    dic = {}
    for i in range(1, 11): #暂定用十种材料
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount' + str(i))
        if material_name:
            dic[i] = {material_name:amount_value}
    for i, values in dic.items():
        for k, v in values.items():
            material = Material(i, k, v, recipe_id)
            material.add()


def material_update(form, recipe_id):
    material_names = Material.query.with_entities(Material.name).filter_by(recipe_id=recipe_id).all() #返回的是[('酱油',), ('辣椒',)]的格式
    materials = []
    for m in material_names: #转化成['酱油', '辣椒']的格式
        materials.append(''.join(m))
    for i in range(1, 11):
        material_name = form.get('material'+str(i))
        amount_value = form.get('amount'+str(i))
        if (material_name) or (amount_value):
            material = Material.query.filter_by(recipe_id=recipe_id, material_number=i).first()
            if material:
                material.update(material_name, amount_value)
            else:
                m = Material(i, material_name, amount_value, recipe_id)
                m.add()


def steps_add(form, recipe_id):
    for i in range(1, 11): # 暂定只用十步
        technique = form.get('step' + str(i) +'_introduce')
        f = request.files.get('step' + str(i) + '_pictures')
        file_formate = 'recipe_' + str(recipe_id) + '_step_' + str(i) + '_'
        if technique:
            filename = upload(f, file_formate)
            steps = Step(i, technique, filename, recipe_id)
            steps.add()


def steps_update(form, recipe_id):
    steps = Step.query.with_entities(Step.step_number).filter_by(recipe_id=recipe_id).all() # 返回如[(1,), （2,), (3,)]的格式
    step_numbers = [s[0] for s in steps] # 转换成[1, 2, 3]的格式
    for i in range(1, 11):
        technique = form.get('step' + str(i) + '_introduce')
        f = request.files.get('step' + str(i) + '_pictures')
        file_formate = 'recipe_' + str(recipe_id) + '_step_' + str(i) + '_'
        print(technique)
        if technique or f:
            filename = upload(f, file_formate)
            s = Step.query.filter_by(recipe_id=recipe_id, step_number=i).first()
            if s:
                os.remove(s.pictures) # 删掉旧图片
                s.update(i, technique, filename)
            else:
                s = Step(i, technique, filename, recipe_id)
                s.add()


@recipe.route('/', methods=['GET'])
@login_required
def index():
    return render_template('recipe.html')


@recipe.route('/recipe_add', methods=['POST'])
@login_required
def recipe_add():
    form = request.form
    f = request.files.get('pictures')
    tips = form.get('tips')
    if f:
        filename = upload(f, None)
        recipe = Recipe(form, filename, tips)
        recipe.add()
        recipe_id = recipe.id
        material_add(form, recipe_id)
        steps_add(form, recipe_id)
    else:
        return redirect(url_for('recipe.index'))
    return redirect(url_for('main.index'))


@recipe.route('/recipe_information', methods=['GET'])
def recipe_information():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('recipe_information.html', recipes=recipes)


@recipe.route('/recipe_edit', methods=['GET'])
@login_required
def recipe_edit():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    material_length = len(recipes.materials.all())
    step_length = len(recipes.steps.all())
    return render_template('recipe_edit.html', recipes=recipes, material_length=material_length, step_length=step_length)


@recipe.route('/recipe_update', methods=['POST'])
@login_required
def recipe_update():
    recipe_id = int(request.args.get('recipe_id'))
    recipe_item = Recipe.query.filter_by(id=recipe_id).first()
    form = request.form
    f = request.files.get('pictures')
    file_formate = 'recipe_' + str(recipe_id) + '_'
    if f:
        os.remove(recipe_item.pictures) # 如果有图片更新，先删除旧图片
        filename = upload(f, file_formate)
    else:
        filename = ''
    recipes = Recipe.query.filter_by(id=recipe_id).first()
    recipes.update(form, filename)
    material_update(form, recipe_id)
    steps_update(form, recipe_id)
    return redirect(url_for('recipe.recipe_information', recipe_id=recipe_id))


@recipe.route('/recipe_delete', methods=['GET'])
@login_required
def recipe_delete():
    recipe_id = int(request.args.get('recipe_id'))
    recipes = Recipe.query.filter_by(id=recipe_id).all()
    materials = Material.query.filter_by(recipe_id=recipe_id)
    steps = Step.query.filter_by(recipe_id=recipe_id)
    for m in materials:
        m.delete_element()
    for s in steps:
        s.delete_element()
    for r in recipes:
        r.delete_element()
    return redirect(url_for('main.index'))