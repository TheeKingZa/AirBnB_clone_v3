#!/usr/bin/python3
"""
index.py endpoint that retrieves the number of each objects
"""
from api.v1.views import app_views  # Import the app_views blueprint
from flask import jsonify  # Import jsonify from Flask for JSON responses
from models import storage  # Import the storage instance


@app_views.route("/status")
def status_ok():
    """
    Defines a route for '/status' that
    returns a JSON response indicating 'OK' status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def obj_stats():
    """
    Defines a route for '/stats' that
    returns JSON response with counts of various objects
    """
    # Count the number of instances for each model and store in a dictionary
    objs = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(objs)  # Return the dictionary as a JSON response
