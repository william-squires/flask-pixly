"""Flask app for Pixly"""
from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Cupcake, DEFAULT_IMAGE

import os

OK_STATUS_CODE = 200
CREATE_STATUS_CODE = 201

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

debug = DebugToolbarExtension(app)

connect_db(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.get("/api/cupcakes")
# def get_all_cupcakes():
#     """
#     Get data on all cupcakes and
#     Return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}
#     """

#     cupcakes = Cupcake.query.all() #TODO: query.order_by(~).all()
#     serialized = [c.serialize() for c in cupcakes]
#     return jsonify(cupcakes=serialized)

# @app.get("/api/cupcakes/<int:cupcake_id>")
# def get_a_single_cupcake(cupcake_id):
#     """
#     Get data on a single cupcake and
#     Return JSON {cupcake: {id, flavor, size, rating, image}}
#     """

#     cupcake = Cupcake.query.get_or_404(cupcake_id)
#     serialized = cupcake.serialize()

#     return jsonify(cupcake=serialized)

@app.post("/api/images")
def upload_file():
    """
    Create a new cupcake! and return JSON
    {cupcake: {id, flavor, size, rating, image}}
    """
    #TODO: request.json directly in instantiation of the cupcake
    #TODO: flavor = request.json["flavor"]
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get('image', DEFAULT_IMAGE)

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), CREATE_STATUS_CODE)

# @app.patch("/api/cupcakes/<int:cupcake_id>")
# def edit_cupcake(cupcake_id):
#     """
#     Update an individual cupcake using data passed in via the body
#     of the request.

#     Return JSON of updated cupcake: {cupcake: {id, flavor, size, rating, image}}
#     """

#     cupcake = Cupcake.query.get_or_404(cupcake_id)

#     cupcake.flavor = request.json.get('flavor', cupcake.flavor)
#     cupcake.size = request.json.get('size', cupcake.size)
#     cupcake.rating = request.json.get('rating', cupcake.rating)
#     cupcake.image = request.json.get('image', cupcake.image) # TODO: change to default image URL rather than their old one (so they can delete an image if they want to)

#     # TODO: `.get()` checks if the key is present, not if there's a truthy value
#     # for the key, so need to add check if 'image' is truthy, and if not, fall
#     # back on default image.

#     db.session.commit()

#     serialized = cupcake.serialize()
#     return(jsonify(cupcake=serialized), OK_STATUS_CODE)

# @app.delete('/api/cupcakes/<int:cupcake_id>')
# def delete_cupcake(cupcake_id):
#     """
#     Delete an individual cupcake.
#     Will return JSON like this: {deleted: [cupcake-id]}
#     """

#     cupcake = Cupcake.query.get_or_404(cupcake_id)

#     db.session.delete(cupcake)
#     db.session.commit()

#     return (jsonify(deleted=cupcake_id), OK_STATUS_CODE)

# @app.get('/')
# def go_to_homepage():
#     """Render the template to the homepage"""
#     return render_template("homepage.html")
