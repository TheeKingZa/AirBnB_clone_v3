#!/usr/bin/python3
""" States view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State

@app_views.route("/states")
def all_states():
    '''Returns a list of all the states'''
    states_list = []
    # Loop through all State instances and convert them to dictionaries
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route("/states/<state_id>")
def state(state_id):
    '''Returns an instance of the specified object'''
    # Retrieve a specific State instance by its ID
    state = storage.get("State", state_id)
    if not state:
        # If the state with the given ID is not found, return a 404 error
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    '''Deletes the specified state'''
    # Retrieve a specific State instance by its ID
    state = storage.get("State", state_id)
    if not state:
        # If the state with the given ID is not found, return a 404 error
        abort(404)
    # Delete the state, save changes, and return an empty response with a 200 status
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route("/states", methods=["POST"])
def create_state():
    '''Creates the specified state'''
    # Check if the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")

    # Check if the JSON data contains the 'name' attribute
    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    # Create a new State instance and set its 'name' attribute
    state = State()
    state.name = request.get_json()['name']
    state.save()

    # Return the created state as JSON with a 201 status
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    '''Updates the state with the id passed'''
    # Retrieve a specific State instance by its ID
    state = storage.get("State", state_id)
    if not state:
        # If the state with the given ID is not found, return a 404 error
        abort(404)

    # Check if the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")

    # Update the state attributes with the values from the JSON data
    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        else:
            setattr(state, k, v)

    # Save the changes and return the updated state as JSON with a 200 status
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
