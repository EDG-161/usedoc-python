import base64
import requests
key = "d6F3Efeqn0m3l0c3"
 
def encrypt(raw ):
    params = {'text':raw, 'pass':key}
    r = requests.post('http://157.245.161.67:3001/enc', data = params)
    return r.text

def decrypt(raw ):
    params = {'text':raw, 'pass':key}
    r = requests.post('http://157.245.161.67:3001/dec', data = params)
    return r.text