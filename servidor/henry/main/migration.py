import pymssql
from decimal import Decimal
from productos.models import *
#information about MSSQL database
BODEGA = 1
USERNAME = 'sa'
PASSWORD = ''
HOST = '192.168.0.102'
DATABASE = 'PYME'

def getDecimal(s):
    s = s.strip()
    s = s.replace(',', '.')
    if s != '':
        return Decimal(s)
def main():
    makeExcel('lista.csv', prod_list())

def excel_prod_list(filename):
    with open(filename) as f:
        lines = f.readlines()
        for l in lines:
            yield l.split(';')

def insertProd(prods, cat):
#asummir prods es una lista de lista, donde cada lista es un prod
#expecifying in order: # codigo, producto, cant, bodega ;precio1, precio2, precio3, precio4, codigo nuevo;
    for prod in prods:
        #create the producto
        print prod
        codigo = prod[0].strip()
        nombre = prod[1].strip()
        prod[4] = prod[4].strip()
        prod[5] = prod[5].strip()
        precio = getDecimal(prod[5]) if getDecimal(prod[5]) != None else getDecimal(prod[4])
        precio2 = getDecimal(prod[4]) if getDecimal(prod[4]) != None else precio#mayorista
        cant = 0
        p, created = Producto.objects.get_or_create(codigo=codigo,
                     nombre=nombre,
                     categoria_id=cat)
        if cat == 1: #flored
            insertContenido(prod=p, cant=cant, precio=precio, precio2=precio2, bodega_id=1) #menorista
            insertContenido(prod=p, cant=cant, precio=precio2, precio2=precio2, bodega_id=2) #mayorista
        else:
            apartir = int(prod[6]) if prod[6].isdigit() else 0
            insertContenido(prod=p, cant=cant, precio=precio, precio2=precio2, bodega_id=1, cant_mayorista=apartir) #menorista
            insertContenido(prod=p, cant=cant, precio=precio2, precio2=precio2, bodega_id=2) #mayorista

        print 'inserted %s, %s' % (codigo, nombre)

def insertContenido(**kwargs):
    cont = Contenido(**kwargs)
    cont.save()
def prod_list():
#a generator that returns a list of list
#expecifying in order: # codigo, producto, cant, bodega;precio1, precio2, precio3;
#sorted by codigo
    conn = pymssql.connect(host=HOST,
                           user=USERNAME,
                           password=PASSWORD,
                           database=DATABASE)
    try:
        cur = conn.cursor()
        getCantidadQuery = """SELECT a.sdo_producto, c.prd_nombre, a.sdo_saldo,
                            a.sdo_empresa, b.prc_v02,b.prc_v03, b.prc_v02i,b.prc_v03i
                              FROM inv_sdobod AS a
                              FULL JOIN inv_lispre AS b ON
                                a.sdo_producto=b.prc_prod and
                                a.sdo_empresa=prc_empresa
                              JOIN tab_producto AS c ON
                                a.sdo_producto=c.prd_codigo and
                                a.sdo_empresa=c.prd_empresa
                              ORDER BY a.sdo_producto
                           """
        #hay que agarrar los precios

        cur.execute(getCantidadQuery)
        row = cur.fetchone()
        while row:
            yield row
            row = cur.fetchone()
    finally:
        conn.close()


def makeExcel(filename, prods):
    with open(filename, 'w') as f:
        content = 'CODIGO; PRODUCTO; CANTIDAD; EMP; P 1; P 2; P 3  \n'
        f.write(content)
        for line in prods:
            print len(line)
            content =  "; ".join(str(f) for f in line)
            content += '\n'
            print content
            f.write(content)

def runQuery(s):
    conn = pymssql.connect(host=HOST,
                           user=USERNAME,
                           password=PASSWORD,
                           database=DATABASE)
    try:
        cur = conn.cursor()
        cur.execute(s)
        row = cur.fetchone()
        while row:
            content =  "; ".join(str(f) for f in row)
            print content
            row = cur.fetchone()
    finally:
        conn.close()

def execute(s):
    conn = pymssql.connect(host=HOST,
                           user=USERNAME,
                           password=PASSWORD,
                           database=DATABASE)
    try:
        cur = conn.cursor()
        cur.execute(s)
    finally:
        conn.close()

def decode(s):
    if type(s) == str:
        return s.decode('latin_1')
    else:
        return str(s).decode('latin_1')

def migrarDeExcel():
    insertProd(excel_prod_list())

def migrarcentro():
    insertProd(excel_prod_list('flores.csv'),1)
    insertProd(excel_prod_list('bisuteria.csv'),2)

def makeNumber(n):
    try:
        return int(float(n))
    except Exception:
        return int(float(n[:-1]))

def putcant(l):
    for line in l:
        print 'inserting', line[0], line[1]
        cont = Contenido.objects.get(bodega_id=1, prod_id=line[0].strip())
        cont.cant_mayorista = makeNumber(line[1])
        cont.save()
def cant():
    putcant(excel_prod_list('bisun.csv'))

def makePriceList(cat):
    prod = Producto.objects.filter(categoria=cat).order_by('nombre')
    with open('price_list.csv', 'w') as f:
        f.write( "Codigo, Nombre, precio mayor, precio mayor2, precio menor, precio menor 2, cantidad mayor\n")
        for p in prod:
            try:
                print p.codigo, p.nombre
                c1 = p.contenido_set.get(bodega_id=1)
                c2 = p.contenido_set.get(bodega_id=2)
                content = ','.join(str(x) for x in [p.codigo, p.nombre, c2.precio, c2.precio2, c1.precio, c2.precio, c1.cant_mayorista])
                f.write(content)
                f.write('\n')
            except Exception:
                pass
if __name__ == '__main__':
    main()
