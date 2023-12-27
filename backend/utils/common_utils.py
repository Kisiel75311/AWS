from flask import jsonify, Response, make_response

def standard_response(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # Check if the result is a Flask Response object (like TestResponse)
        if isinstance(result, Response):
            return result
        if isinstance(result, tuple):
            data, status_code = result
        else:
            data, status_code = result, 200
        return jsonify({'data': data, 'error': None}), status_code
    wrapper.__name__ = func.__name__
    return wrapper