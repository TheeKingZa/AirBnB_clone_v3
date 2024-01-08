#!/usr/bin/python3
""" Creates a Flask web service"""

from flask import Flask, make_response, jsonify
import os import getenv
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

# Create a Flask web application instance
app = Flask(__name__)

# Enable CORS for the entire API
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# Disable strict slashes at the end of routes
app.url_map.strict_slashes = False

# Register the blueprint containing API routes
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """Removes the current SQLAlchemy session for tear down"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 error with 'Not Found' error message"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    """ Handles 400 errors with an 'error' message"""
    return make_response(jsonify({'error': error.description}), 400)


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
