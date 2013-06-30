from flask import render_template, request, jsonify, redirect, session, g, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.views import MethodView

from sqlalchemy import func

import json

from app import app, db, lm, oid
from forms import LoginForm
from models import User, Recipe, RecipeIngredient, ROLE_USER, ROLE_ADMIN

class RecipeAPI(MethodView):

    def get(self, r_id):
        user = g.user
        searchstr = request.args.get('data')
        searchtype = request.args.get('type')
        if searchstr is None:
            recipes = g.user.recipes
        else:
            if searchtype == 'name':
                recipes = db.session.query(Recipe).join(User.recipes).filter(func.substr(func.lower(Recipe.name), 1, len(searchstr)) == func.lower(searchstr)).all()
            else:
                searchstr = searchstr.lower()
                #recipes = db.session.query(Recipe).filter(Recipe.user_id == g.user.id).filter(Recipe.id == RecipeIngredient.parent_id).join(Recipe.ingredients).filter(func.lower(RecipeIngredient.name) == searchstr).all()
                recipes = db.session.query(Recipe).join(User.recipes).filter(Recipe.user_id == g.user.id).join(Recipe.ingredients).filter(func.lower(RecipeIngredient.name)==searchstr).all()
                #recipes = db.session.query(User, Recipe).filter(User.id == g.user.id).join(Recipe.ingredients).filter(RecipeIngredient.name==searchstr).all()
                #recipes = db.session.query(Recipe).join(User.recipes, User.id==g.user.id).join(Recipe.ingredients).filter(RecipeIngredient.name==searchstr).all()
        return jsonify(items=[recipe.to_json() for recipe in recipes])
    
    #put means a record was updated and sent
    def put(self, r_id):
        data = json.loads(request.data)
        recipe = db.session.query(Recipe).filter_by(id=r_id).first()
        recipe.name = data["name"]
        #recipe.ingredients = data["ingredients"]
        for rec in recipe.ingredients:
            db.session.delete(rec)
        for ingredient in data["ingredients"]:
            irec = RecipeIngredient()
            irec.name = ingredient
            recipe.ingredients.append(irec)
        recipe.instructions = data["instructions"]
        recipe.author = data["author"]
        #maybe don't do this
        db.session.add(recipe)
        try:
            db.session.commit()
        except Exception,e:
            print "error adding new record"
            db.session.rollback()
        return ""

    def delete(self, r_id):
        record = db.session.query(Recipe).filter_by(id=r_id).first()
        db.session.delete(record)
        try:
            db.session.commit()
        except Exception,e:
            print "error adding new record"
            db.session.rollback()
        return ""

    #post means a new record was sent
    def post(self):
        data = json.loads(request.data)
        user = g.user
        recipe = Recipe()
        recipe.name = data["name"]
        for ingredient in data["ingredients"]:
            irec = RecipeIngredient()
            irec.name = ingredient
            recipe.ingredients.append(irec)
        recipe.instructions = data["instructions"]
        recipe.author = data["author"]
        user.recipes.append(recipe)
        #db.session.add(recipe)
        try:
            db.session.commit()
        except Exception,e:
            print "error adding new record"
            db.session.rollback()
        return ""

recipe_view = RecipeAPI.as_view('recipes')
app.add_url_rule('/recipes/', view_func=recipe_view, methods=['GET',], defaults={"r_id": None})
app.add_url_rule('/recipes', view_func=recipe_view, methods=['POST',])
app.add_url_rule('/recipes/<int:r_id>', view_func=recipe_view, methods=['PUT', 'DELETE'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route("/")
@app.route("/index")
def index():
    user = g.user
    return render_template('index.html', user=user)

@app.route('/logout')
def logout():
    print g.user.nickname
    logout_user()
    return redirect(url_for('index'))
    
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
