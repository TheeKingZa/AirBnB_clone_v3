#!/usr/bin/python3
"""Create a route `/status` on the object app_views.

Return: JSON: "status": "OK"

"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', __name__, url_prefix="/api/v1")
def api_status():
    """ Returns a JSON status for RESTful API."""
    status = {'status': 'OK'}
    return jsonify(response)
