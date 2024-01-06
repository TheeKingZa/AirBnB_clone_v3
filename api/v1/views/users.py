#!/usr/bin/python3
"""
Users app view
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


# Route to retrieve the list of all User objects
@app_views.route("/users", methods=['GET'])
def all_users():
    """Retrieves the list of all User objects"""
    users_list = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users_list)


# Route to retrieve a specific User object by user_id
@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


# Route to delete a specific User object by user_id
@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


# Route to create a new User object
@app_views.route("/users", methods=['POST'])
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


# Route to update a specific User object by user_id
@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    # Update the User object with the provided data
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
