import hashlib
import base64

def _char_filter(password, unavailable_char):
    for char in unavailable_char:
        password = password.replace(char.encode(),''.encode())
    return password
    
def generate(site, user, master_password, max_length=0, unavailable_char=''):
    password = _char_filter(base64.b64encode(hashlib.sha512((site + user + master_password).encode()).hexdigest().encode()), unavailable_char)
    if max_length == 0:
        return password.decode()
    else:
        return password[0:max_length].decode()
        
