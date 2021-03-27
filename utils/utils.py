def check_required_fields(data, required_fields):
    errors = {}
    for item in required_fields:
        if item not in data.keys():
            errors[item] = [
                "This field is required"
            ] 
    return errors

def gen_response(error, success, message="", data={}):
    return {
        "error": error,
        "success": success,
        "message": message,
        "data": data
    }
