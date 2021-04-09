from flask import make_response, jsonify

def error_response(code, message, err):
    return make_response(jsonify({"msg": message, "error": err}), code)


def success_response(code, message, data):
    return make_response(jsonify({"msg": message, "data": data}), code)
