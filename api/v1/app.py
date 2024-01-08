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


if __name__ == '__main__':
    # Check if the script is being run directly
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        # If environment variables for host and port are set, use them
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        # Otherwise, run the app on host '0.0.0.0' and port 5000
        app.run(host='0.0.0.0', port=5000, threaded=True)
