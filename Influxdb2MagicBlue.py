# -*- coding: utf-8 -*-
from magicbluelib import MagicBlue
import matplotlib.pyplot as plt
import time
import numpy as np
import sys, getopt
from influxdb import InfluxDBClient
__author__ = 'nboettcher@udec.cl'


def cmap2hex(mag=0.5,cmax=1,cmin=0,cmap='jet'):
    color = plt.get_cmap(cmap)
    #normalize
    x = float(mag - cmin) / float(cmax - cmin)
    # obtiene el rgb sin alpha normalizado
    rgbNorm=color(x)[:3]
    # lo pasa a escala de 0 a 255
    rgbFull=np.mat(rgbNorm)*255
    # redondea los float y los convierte a int
    rgbInt= np.rint(rgbFull).astype(int)
    # convierte la matriz a list
    return np.asarray(rgbInt).reshape(-1)

def connect():
    bulb = MagicBlue(mac)
    bulb.connect()
    return bulb

def change_color(num=100):
    bulb=connect()
    bulb.turn_on()
    colorRgb=cmap2hex(num,100)
    bulb.set_color(colorRgb)
    bulb.disconnect()


def read_edge_influxdb(hostA, hostB, db='sdn', value='bw'):
    client = InfluxDBClient(address, port, user, password, db)
    result = client.query('select '+value+' from ' + table + ' where topology = \'' + topology + '\' and ((src=\'' + hostA + '\' and dst=\'' + hostB + '\') or (src = \'' + hostB + '\' and dst = \'' + hostA + '\')) order by time desc limit 1;')
    valores = result._get_series()[0].get('values')
    print("Last input {}".format(valores[0][1]))
    # get value
    return valores[0][1]

def main():
    try:
        # while True:
            #bw=lee_influxdb('bw','bulb',-1)
        bw=read_edge_influxdb(src,dst,db)
        # time.sleep(1)
        change_color(bw)
    except:
        print('\nEl programa se ha cerrado inesperadamente')

if __name__ == "__main__":
    address = 'localhost'
    port = '8086'
    user = 'admin'
    password = 'admin'
    db='sdn'
    table='edges'
    topology='ATT'
    mac='c4:bd:7c:27:89:bf'
    src='0'
    dst='2'

    try:
        myopts, args = getopt.getopt(sys.argv[1:], "ha:P:u:p:D:t:T:s:d:m:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -a address -P port -u user -P password -D database -t table -T topology -s source -d destination -m mac" % sys.argv[0])
        sys.exit(2)

    for o, a in myopts:
        if o == '-h':
            print('Influxdb2MagicBlue.py -a <address> -p <port> -u <user> -P <password> -D <database> -t <table> -T <topology> -s <source> -d <destination> -m <mac>')
            sys.exit()
        elif o == '-a':
            address = a
        elif o == '-p':
            port = a
        elif o == '-u':
            user = a
        elif o == '-P':
            password = a
        elif o == '-D':
            db = a
        elif o == '-t':
            table = a
        elif o == '-T':
            topology = a
        elif o == '-s':
            src = a
        elif o == '-d':
            dst = a
        elif o == '-m':
            mac = a

    main()
