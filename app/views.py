from flask import render_template, request, jsonify

from app import app, db

from models import User, Recipe, Post


@app.route("/recipes")
def recipes():
    recipes = db.session.query(Recipe).all()
    
    return jsonify(items=[recipe.to_json() for recipe in recipes])

@app.route("/users")
def users():
    #recs = {}
    #for key, value in db.session.query(User).all():
    #    users[key] = value
    users = db.session.query(User).all()
    #for user in users:
        #print user.to_json()
    #print users
    #oblist = [user.to_json() for user in users]
    #print oblist
    #print jsonify(oblist)
    return jsonify(items=[user.to_json() for user in users])

@app.route("/")
def index():
    return render_template('index.html')
