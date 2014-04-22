# -*' coding: utf8 -*-
from datetime import *

def convertir(inpath, outpath):
    with open(inpath, 'r') as infile:
        with open(outpath, 'w') as outfile:
            for line in infile:

                medidor = line[:10]
                validacion = line[10:11]
                concepto = line[11:15]
                suministro = line[15:25]
                nombre = line[25:45]
                direccion = line[45:70]
                categoria = line[70:75]
                digMedidor = line[75:76]
                estado_actual = line[76:85]
                consumo_actual = line[85:94]
                operador = line[94:96]
                dia = line[96:98]
                mes = line[98:100]
                anio = line[100:104]
                hora = line[104:110]
                novedades = line[110:112]

                f_actual = date(int(anio),int(mes),int(dia))

                outfile.write(str(int(suministro.strip())) + ',' 
                    + medidor.strip() + ',' 
                    + concepto.strip('0') + ','
                    + f_actual.strftime('%d-%m-%Y') + ',' 
                    + estado_actual.strip() + ',' 
                    + consumo_actual.strip() + '\n')



inputfile = '/home/dooky/Desarrollo/FEDECOBA/Archivos Consumos/lecturasCEAL.txt'
outputfile = '/home/dooky/Desarrollo/FEDECOBA/Archivos Consumos/estandarCEAL.txt'
convertir(inputfile, outputfile)