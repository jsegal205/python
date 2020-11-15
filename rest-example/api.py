import flask
import json
from flask import request, Response, jsonify

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
    return jsonify(sorted(recipes, key=lambda r: r["id"]))


@app.route("/recipe/<int:id>", methods=["GET"])
def recipe_single(id):
    for recipe in recipes:
        if recipe["id"] == id:
            return Response(json.dumps(recipe), status=200)

    return Response("No Recipe found with id of {}".format(id), status=404)


@app.route("/recipe", methods=["POST"])
def recipe_add():
    # TODO: add auth
    body = json.loads(str(request.data, encoding='utf-8'))

    next_id = len(recipes) + 1
    new_recipe = {
        "id": next_id,
        "title": body["title"],
        "ingredients": body["ingredients"],
        "directions": body["directions"]
    }
    recipes.append(new_recipe)

    return Response(json.dumps(new_recipe), status=201, mimetype='application/json')


@app.route("/recipe/<int:id>", methods=["DELETE"])
def recipe_remove(id):
    # TODO: add auth, combine with PUT method
    for recipe in recipes:
        if recipe["id"] == id:
            recipes.remove(recipe)
            return Response("Recipe with id of `{}` has been removed".format(id), status=200)

    return Response("No Recipe found with id of {}".format(id), status=404)


@app.route("/recipe/<int:id>", methods=["PUT"])
def recipe_update(id):
    # TODO: add auth, combine with DELETE method
    for recipe in recipes:
        if recipe["id"] == id:
            body = json.loads(str(request.data, encoding='utf-8'))

            # TODO: fallback to recipe prop if not passed in body
            updated_recipe = {
                "id": recipe["id"],
                "title": body["title"],
                "ingredients": body["ingredients"],
                "directions": body["directions"]
            }

            recipes.remove(recipe)
            recipes.append(updated_recipe)
            return Response(json.dumps(updated_recipe), status=200, mimetype='application/json')

    return Response("No Recipe found with id of {}".format(id), status=404)


app.run()
