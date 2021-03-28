from parkinglot.models import Parking


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

def get_avalable_slots(parking_lot_ref, total_parking_slots):
    filled_slots = Parking.objects.filter(parking_lot_ref=parking_lot_ref, payment_status=False).count()
    return total_parking_slots - filled_slots
