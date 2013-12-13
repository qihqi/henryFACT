import pymssql
from decimal import Decimal
#information about MSSQL database
BODEGA = 1
USERNAME = 'sa'
PASSWORD = ''
HOST = '192.168.0.102'
DATABASE = 'PYME'


def main():
    makeExcel('lista.csv', prod_list())

def excel_prod_list():
    with open('lista_poli.csv') as f:
        lines = f.readlines()
        for l in lines:
            yield l.split(';')

def insertProd(prods):
#asummir prods es una lista de lista, donde cada lista es un prod
#expecifying in order: # codigo, producto, cant, bodega ;precio1, precio2, precio3, precio4, codigo nuevo;
    for prod in prods:
        #create the producto
        codigo = prod[8]
        cod_viejo = prod[0]
        nombre = prod[1]
        precio = Decimal(prod[4]) if Decimal(prod[4]) != 0 else Decimal(prod[5])
        cant = 0
        p = Producto(codigo_barra=int(cod_viejo),
                     codigo=codigo,
                     nombre=nombre)
        p.save()

        cont = Contenido(prod=p, cant=cant, precio=precio, precio2=precio, bodega=BODEGA)
        cont.save()
        print 'inserted %s, %s' % codigo, nombre


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


if __name__ == '__main__':
    main()
