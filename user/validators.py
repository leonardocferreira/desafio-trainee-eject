import re
from validate_docbr import CPF

def valid_cpf(cpf_number):
    cpf_clean = re.sub(r'\D', '', str(cpf_number)) # faz retornar apenas os numeros
    cpf = CPF()
    cpf_valido = cpf.validate(cpf_clean)
    return cpf_valido

def valid_cep(cep_number):
    model_cep = '^\d{5}-\d{3}$'
    cep = str(cep_number)
    result = re.match(model_cep, cep)
    return bool(result)
    
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

def password_match(password, confirm_password):
    return password == confirm_password