import pymssql
from datetime import datetime
from productos.models import *
from django.db import IntegrityError
from clientes.models import Cliente
#information about MSSQL database
BODEGA = 1
USERNAME = 'sa'
PASSWORD = ''
HOST = '192.168.0.10'
DATABASE = 'PYME'

def insertCliente(nombre_comp, direccion, telf, ruc):
    try:
        tokens = nombre_comp.strip().split()
        apellidos = ' '.join(tokens[:2]).decode('latin_1')
        nombres = ' '.join(tokens[2:]).decode('latin_1')
    except UnicodeEncodeError:
        print( (str(apellidos) + '; ' + str(nombres) + '; ' + str(ruc) + '; '
              + str(telf) + '; ' + str(direccion.decode('latin_1'))  + '\n'))
    try:
        cliente = Cliente(codigo=ruc.strip(),
                          apellidos=apellidos,
                          nombres=nombres,
                          direccion=direccion.decode('latin_1'),
                          telefono=telf.strip(),
                          tipo='B',
                          cliente_desde=datetime.today())
        cliente.save()
    except Warning:
        name = nombres.replace('\xD1', 'N')
        name = name.replace('\xC8', 'A')
        print nombre_comp, direccion
        app = apellidos.replace('\xD1', 'N')
        app = app.replace('\xC8', 'A')
        dire = direccion.replace('\xD1', 'N')
        dire = dire.replace('\xC8', 'A')
        dire = dire.replace('\xBA', 'o')
        dire = dire.replace('\xA6', '')
        dire = dire.replace('\xAA', '')
        dire = dire.replace('\xB7', '')
        cliente = Cliente(codigo=ruc,
                          apellidos=app,
                          nombres=name,
                          direccion=dire,
                          telefono=telf,
                          tipo='A',
                          cliente_desde=datetime.today())
        cliente.save()
def main():
    conn = pymssql.connect(host=HOST,
                           user=USERNAME,
                           password=PASSWORD,
                           database=DATABASE)
    try:
        cur = conn.cursor()
        clienteQuery = """select per_nombre, per_direccion, per_telefono, per_ciruc from tab_persona"""
        cur.execute(clienteQuery)
        row = cur.fetchone()
        while row:
	        insertCliente(row[0], row[1], row[2], row[3])
	        row = cur.fetchone()


    finally:
        conn.close()

def fromFile():
    with open('excel/prod.csv') as f:
        lines = f.readlines();
        for line in lines:
            row = line.split(';')
            insertOneProd(row[1], row[2])


if __name__ == '__main__':
    fromFile()
