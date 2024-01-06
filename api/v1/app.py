#!/usr/bin/python3
""" Creates a Flask web service"""

from flask import Flask, make_response, jsonify
import os
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)  # Create a Flask web application instance
CORS(app, resources={"/api/*": {"origins": "0.0.0.0"}})  # Enable CORS for the entire API
app.url_map.strict_slashes = False  # Disable strict slashes at the end of routes
app.register_blueprint(app_views)  # Register the blueprint containing API routes

@app.teardown_appcontext
def tear_down(self):
    """ Removes the current SQLAlchemy session when the app context is torn down"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Handles 404 errors by returning a JSON response with an 'error' message"""
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ Handles 400 errors by returning a JSON response with an 'error' message"""
    return make_response(jsonify({'error': error.description}), 400)

if __name__ == "__main__":
    # Check if the script is being run directly
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        # If environment variables for host and port are set, use them
        app.run(host=os.getenv("HBNB_API_HOST"), port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        # Otherwise, run the app on host '0.0.0.0' and port 5000
        app.run(host='0.0.0.0', port=5000, threaded=True)
