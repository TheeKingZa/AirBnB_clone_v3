#!/usr/bin/python3
"""Handles all default RESTful API tasks for reviews."""

from flask import abort, jsonify, request
from models.review import Review
from api.v1.views import app_views
from models import storage


# Retrieves the list of all Review objects of a Place:
# GET /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    # Return 404 error if the Place object is not found
    if place is None:
        abort(404)
    # Otherwise, retrieve and return the list of Review objects in JSON format
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


# Retrieves a Review object: GET /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get(Review, review_id)
    # Return 404 error if the Review object is not found
    if review is None:
        abort(404)
    # Otherwise, return the Review object in JSON format
    return jsonify(review.to_dict())


# Deletes a Review object: DELETE /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    # Delete the Review object from the storage and save changes
    if review:
        storage.delete(review)
        storage.save()
        # Returns an empty dictionary with the status code 200
        return jsonify({}), 200
    else:
        # Otherwise, return 404 error if Review object is not found
        abort(404)


# Creates a Review: POST /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    # Get the JSON data from the request
    data = request.get_json()

    # If place_id is not linked to any Place object, raise 404 error
    place = storage.get(Place, place_id)
    if place is None:
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

    # If the dictionary doesn’t contain the key text,
    # raise a 400 error with the message 'Missing text'
    if 'text' not in data:
        abort(400, 'Missing text')

    # Create a new Review object with the given data
    review = Review(place_id=place_id, user_id=data['user_id'],
                    text=data['text'])
    review.save()

    # Return the new Review object with status code 201 in JSON format
    return jsonify(review.to_dict()), 201


# Updates a Review object: PUT /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)
    # If review_id is not linked to any Review object, raise 404 error
    if review is None:
        abort(404)

    # Otherwise, use request.get_json from Flask to transform
    # HTTP request to a dictionary
    if review:
        # Get the JSON data from the request
        data = request.get_json()

        # Return 400 error if the request data is not in JSON format
        if data is None:
            abort(400, 'Not a JSON')

        # Update the attributes of the Review object with the JSON data
        for key, value in data.items():
            attr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            if key not in attr:
                setattr(review, key, value)
        review.save()

        # Return the updated Review object in JSON format with 200 status code
        return jsonify(review.to_dict()), 200
