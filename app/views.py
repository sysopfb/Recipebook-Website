from flask import render_template, request, jsonify

from flask.views import MethodView

from sqlalchemy import func

import json

from app import app, db

from models import Recipe


class RecipeAPI(MethodView):

    def get(self, r_id):
        searchstr = request.args.get('data')
        searchtype = request.args.get('type')
        if searchstr is None:
            recipes = db.session.query(Recipe).all()
        else:
            if searchtype == 'name':
                recipes = db.session.query(Recipe).filter(func.substr(func.lower(Recipe.name), 1, len(searchstr)) == func.lower(searchstr)).all()
            else:
                searchstr = searchstr.lower()
                recipes = db.session.query(Recipe).all()
                #Ugly hack...
                #TODO: Change the database models to use a list of tables of a new model
                recipe_ids = [r.id for r in recipes if searchstr in map(lambda x: x.lower(), r.ingredients)]
                recipes = db.session.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()

        return jsonify(items=[recipe.to_json() for recipe in recipes])
    
    #put means a record was updated and sent
    def put(self, r_id):
        data = json.loads(request.data)
        recipe = db.session.query(Recipe).filter_by(id=r_id).first()
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

recipe_view = RecipeAPI.as_view('recipes')
app.add_url_rule('/recipes/', view_func=recipe_view, methods=['GET',], defaults={"r_id": None})
app.add_url_rule('/recipes', view_func=recipe_view, methods=['POST',])
app.add_url_rule('/recipes/<int:r_id>', view_func=recipe_view, methods=['PUT', 'DELETE'])
'''
@app.route("/users")
def users():
    users = db.session.query(User).all()
    return jsonify(items=[user.to_json() for user in users])
'''
@app.route("/")
def index():
    return render_template('index.html')
