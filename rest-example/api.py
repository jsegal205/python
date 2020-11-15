import flask
import json
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"]

recipes = [
    {
        "id": 1,
        "title": "Chocolate Chip Cookies",
        "ingredients": "flour, sugar, eggs, chocolate chips",
        "directions": "mix things, bake at 350F for 9 minutes"
    },
    {
        "id": 2,
        "title": "Scrambled eggs",
        "ingredients": "eggs",
        "directions": "crack eggs, heat in a pan, scramble them"
    }
]


@app.route("/", methods=["GET"])
def home():
    return "this is the home route for JIMBO's jellybean extravaganza"


@app.route("/recipes", methods=["GET"])
def recipes_all():
    return jsonify(recipes)


@app.route("/recipe/<int:id>", methods=["GET"])
def recipe_single(id):
    for recipe in recipes:
        if recipe["id"] == id:
            return recipe

    return "No Recipe found with id of {}".format(id)


@app.route("/recipe", methods=["POST"])
def recipe_add():
    body = json.loads(str(request.data, encoding='utf-8'))

    next_id = len(recipes) + 1
    new_recipe = {
        "id": next_id,
        "title": body["title"],
        "ingredients": body["ingredients"],
        "directions": body["directions"]
    }
    recipes.append(new_recipe)

    return new_recipe


app.run()
