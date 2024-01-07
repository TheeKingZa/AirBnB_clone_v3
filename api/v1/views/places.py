#!/usr/bin/python3
"""Handles all default RESTful API tasks for places."""

from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Retrieves the list of all Place objects of a City:
# GET /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    # Return 404 error if the City object is not found
    if city is None:
        abort(404)
    # Otherwise, retrieve and return the list of Place objects in JSON format
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


# Retrieves a Place object: GET /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    # Return 404 error if the Place object is not found
    if place is None:
        abort(404)
    # Otherwise, return the Place object in JSON format
    return jsonify(place.to_dict())


# Deletes a Place object: DELETE /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    # Delete the Place object from the storage and save changes
    if place:
        storage.delete(place)
        storage.save()
        # Returns an empty dictionary with the status code 200
        return jsonify({}), 200
    else:
        # Otherwise, return 404 error if Place object is not found
        abort(404)


# Creates a Place: POST /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    # Get the JSON data from the request
    data = request.get_json()

    # If city_id is not linked to any City object, raise 404 error
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # If HTTP request body is not valid JSON, 400 error is raised
    # with the message 'Not a JSON'
    if data is None:
        abort(400, 'Not a JSON')

    # If the dictionary doesn’t contain the key user_id,
    # raise a 400 error with the message 'Missing user_id'
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    # If the user_id is not linked to any User object, raise a 404 error
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    # If the dictionary doesn’t contain the key name,
    # raise a 400 error with the message 'Missing name'
    if 'name' not in data:
        abort(400, 'Missing name')

    # Create a new Place object with the given data
    place = Place(city_id=city_id, user_id=data['user_id'], name=data['name'])
    place.save()

    # Return the new Place object with status code 201 in JSON format
    return jsonify(place.to_dict()), 201


# Updates a Place object: PUT /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    # If place_id is not linked to any Place object, raise 404 error
    if place is None:
        abort(404)

    # Otherwise, use request.get_json from Flask to transform
    # HTTP request to a dictionary
    if place:
        # Get the JSON data from the request
        data = request.get_json()

        # Return 400 error if the request data is not in JSON format
        if data is None:
            abort(400, 'Not a JSON')

        # Update the attributes of the Place object with the JSON data
        for key, value in data.items():
            attr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            if key not in attr:
                setattr(place, key, value)
        place.save()

        # Return the updated Place object in JSON format with 200 status code
        return jsonify(place.to_dict()), 200
