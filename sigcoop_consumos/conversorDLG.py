# -*' coding: utf8 -*-
from datetime import *

def convertir(inpath, outpath):
    with open(inpath, 'r') as infile:
        with open(outpath, 'w') as outfile:
            for line in infile:
                (calle,_,resto) = line.partition(':')
                (ruta,_,resto) = resto.partition(':')
                (numero,_,resto) = resto.partition(':')
                (algo,_,resto) = resto.partition(':')
                (medidor,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (estado_anterior,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (fecha,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition('::')
                (estado_actual,_,resto) = resto.partition(':')
                suministro = calle + '.' + ruta + '.' + numero + '.' + algo 
                # print suministro, ',', medidor, ',', consumo_anterior, ',', fecha, ',', consumo_actual

                (dia,_,resto) = fecha.partition('/')
                (mes,_,anio) = resto.partition('/')

                f_actual = date(int(anio),int(mes),int(dia))
                f_anterior = date(int(anio),int(mes)-1,int(dia))
                c_anterior = int(estado_anterior)
                c_actual = int(estado_actual)
                c_neto = c_actual - c_anterior

                outfile.write(suministro + ',' 
                    + medidor + ',' 
                    + str(1) + ','
                    + f_actual.strftime('%d-%m-%Y') + ',' 
                    + estado_actual + ',' 
                    + str(c_neto) + '\n')



inputfile = 'lecturasDLG.txt'
outputfile = 'estandarDLG.txt'
convertir(inputfile, outputfile)