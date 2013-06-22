from flask import render_template, request, jsonify

from flask.views import MethodView

from sqlalchemy import func

import json

from app import app, db

from models import Recipe


class RecipeAPI(MethodView):

    def get(self):
        searchstr = request.args.get('data')
        if searchstr is None:
            recipes = db.session.query(Recipe).all()
        else:
            recipes = db.session.query(Recipe).filter(func.substr(func.lower(Recipe.name), 1, len(searchstr)) == func.lower(searchstr)).all()

        return jsonify(items=[recipe.to_json() for recipe in recipes])
    
    #put means a record was updated and sent
    def put(self):
        return ""

    #post means a new record was sent
    def post(self):
        data = json.loads(request.data)
        recipe = Recipe()
        recipe.name = data["name"]
        recipe.ingredients = data["ingredients"]
        recipe.instructions = data["instructions"]
        recipe.author = data["author"]
        db.session.add(recipe)
        try:
            db.session.commit()
        except Exception,e:
            print "error adding new record"
            db.session.rollback()
        return ""


app.add_url_rule('/recipes', view_func=RecipeAPI.as_view('recipes'))
'''
@app.route("/users")
def users():
    users = db.session.query(User).all()
    return jsonify(items=[user.to_json() for user in users])
'''
@app.route("/")
def index():
    return render_template('index.html')
