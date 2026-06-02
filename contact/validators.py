import re

def valid_phone_number(phone_number):
    model_phone = '^\d{2} \d{1} \d{4}-\d{4}$'
    phone = str(phone_number)
    result = re.match(model_phone, phone)
    return bool(result)

def valid_name(full_name):
    model_name = '^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)+$'
    if len(full_name) < 2:
        return False
    result = re.match(model_name, full_name)
    return bool(result)