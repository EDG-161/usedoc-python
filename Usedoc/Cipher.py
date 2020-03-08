import base64
import requests
key = "d6F3Efeqn0m3l0c3"
 
def encrypt(raw ):
    params = {'text':raw, 'pass':key}
    r = requests.post('https://www.usedoc.ml/enc', data = params)
    return r.text

def decrypt(raw ):
    params = {'text':raw, 'pass':key}
    r = requests.post('https://www.usedoc.ml/dec', data = params)
    return r.text