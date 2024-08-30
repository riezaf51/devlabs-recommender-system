import json
from flask import Response

def success_response(data=None, message="Success", status_code=200):
    """
    Return a standardized success response.

    :param data: The data to include in the response.
    :param message: A message to include in the response.
    :param status_code: The HTTP status code for the response.
    :return: A JSON response with the specified status code.
    """
    response = {
        "success": True,
        "message": message,
        "code": status_code,
        "data": data
    }
    json_data = json.dumps(response, indent=4)
    return Response(json_data, mimetype='application/json'), status_code

def error_response(message="An error occurred", status_code=400):
    """
    Return a standardized error response.

    :param message: A message to include in the response.
    :param status_code: The HTTP status code for the response.
    :return: A JSON response with the specified status code.
    """
    response = {
        "success": False,
        "message": message,
        "code": status_code,
    }
    json_data = json.dumps(response, indent=4)
    return Response(json_data, mimetype='application/json'), status_code
