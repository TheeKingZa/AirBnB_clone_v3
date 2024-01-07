#!/usr/bin/python3
"""Handles all default RESTful API task for amenities."""

from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Retrieves the list of all Amenity objects: GET /api/v1/amenities
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


# Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    # Return 404 error if the Amenity object is not found
    if amenity is None:
        abort(404)
    # Otherwise, return the Amenity object in JSON format
    return jsonify(amenity.to_dict())


# Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    # Delete the Amenity object from the storage and save changes
    if amenity:
        storage.delete(amenity)
        storage.save()
        # Returns an empty dictionary with the status code 200
        return jsonify({}), 200
    else:
        # Otherwise, return 404 error if Amenity object is not found
        abort(404)


# Creates a Amenity: POST /api/v1/amenities
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object"""
    # Get the JSON data from the request
    data = request.get_json()

    # If HTTP request body is not valid JSON, 400 error is raised
    # with the message 'Not a JSON'
    if data is None:
        abort(400, 'Not a JSON')

    # If the dictionary doesn’t contain the key name,
    # 400 error with the message Missing name is raised
    if 'name' not in data:
        abort(400, 'Missing name')

    # Return new Amenity with status code 201 in JSON format
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    # If amenity_id is not linked to Amenity object, raise 404 error
    if amenity is None:
        abort(404)

    # Otherwise, use request.get_json from Flask to transform
    # HTTP request to a dictionary
    if amenity:
        # Get the JSON data from the request
        data = request.get_json()

        # Return 400 error if the request data is not in JSON format
        if data is None:
            abort(400, 'Not a JSON')

        # Update the attributes of the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()

        # Return the updated Amenity object in JSON format with 200 status code
        return jsonify(amenity.to_dict()), 200
