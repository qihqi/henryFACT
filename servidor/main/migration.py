import pymssql

#information about MSSQL database
BODEGA = 0
USERNAME = 'sa'
PASSWORD = ''
HOST = '192.168.0.10'
DATABASE = 'PYME'

def insertOneProd(f, codigo, nombre, precio, bodega):
    f.write( (str(bodega) + '; ' + str(codigo) + '; ' + str(precio) + '; ' + str(nombre)+ '\n'))


def insertItem(f, prod, cantidad, bodega):
    f.write( (str(bodega) + '; ' + str(prod) + '; ' + str(cantidad) + '\n'))

def main():
    conn = pymssql.connect(host=HOST,
                           user=USERNAME,
                           password=PASSWORD,
                           database=DATABASE)
    try:
        cur = conn.cursor()
        getProdQuery = """SELECT prd_codigo, prd_nombre, prd_empresa FROM tab_producto"""
        cur.execute(getProdQuery)
        row = cur.fetchone()
        f = open("prod.csv", "w")
        while row:
            insertOneProd(f, row[0], row[1], 0,row[2])
            row = cur.fetchone()
        f.close()
        getCantidadQuery = """SELECT sdo_producto, sdo_saldo, sdo_empresa FROM inv_sdobod"""


        cur.execute(getProdQuery)
        row = cur.fetchone()
        g = open('cant.csv', "w")
        while row:
            insertItem(g, row[0], row[1], row[2])
            row = cur.fetchone()
        g.close()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
