#api para comunicar por internet
import hashlib
import requests
import json
from decimal import Decimal
#enviar datos, destino = full address
#datos = datos en json
def parse(datos):
    obj = json.loads(datos)
    header = obj['header']
    content = [(Decimal(c), d) for c, d in obj['content']]
    return header, content
def serialize(header, content):
    return json.dumps({'header' : header, 'content' : content})

def enviar(destino, datos):
   #get the csrf token from django

    r = requests.get(destino)
    if r.status_code != 200:
        return -1
   #make a post con el token
    r = requests.post(destino,
                     data={'msg' : datos, 'key' : generar_crypt(datos)})
    if r.status_code == 200:
        resp_map = json.loads(r.text)
        num = resp_map.get('num')
        return num if num else -1
    return -1

SECRET_KEY = '05316900911JNHSDnojodasApurateHelenNathy' #cualquier cosa

def generar_crypt(data):
   m = hashlib.sha1()
   m.update(SECRET_KEY + data)
   return m.hexdigest()

def verificar_crypt(data, key):
    return generar_crypt(data) == key

