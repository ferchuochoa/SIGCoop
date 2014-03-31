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
                (consumo_anterior,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (fecha,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition(':')
                (_,_,resto) = resto.partition('::')
                (consumo_actual,_,resto) = resto.partition(':')
                suministro = calle + '.' + ruta + '.' + numero + '.' + algo 
                # print suministro, ',', medidor, ',', consumo_anterior, ',', fecha, ',', consumo_actual

                (dia,_,resto) = fecha.partition('/')
                (mes,_,anio) = resto.partition('/')

                f_actual = date(int(anio),int(mes),int(dia))
                f_anterior = date(int(anio),int(mes)-1,int(dia))
                period = mes + '/' + anio
                c_anterior = int(consumo_anterior)
                c_actual = int(consumo_actual)
                c_neto = c_actual - c_anterior

                outfile.write(suministro + ',' 
                    + medidor + ',' 
                    + period + ',' 
                    + f_actual.strftime('%d-%m-%Y') + ',' 
                    + consumo_actual + ',' 
                    + str(c_neto) + '\n')





# def main(argv):
#     inputfile = ''
#     outputfile = ''
#     try:
#         opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#     except getopt.GetoptError:
#         print 'conversorDLG.py -i <inputfile> -o <outputfile>'
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print 'conversorDLG.py -i <inputfile> -o <outputfile>'
#             sys.exit()
#         elif opt in ("-i", "--ifile"):
#             inputfile = arg
#         elif opt in ("-o", "--ofile"):
#             outputfile = arg

#     convertir(inputfile, outputfile)


# if __name__ == "__main__":
#    main(sys.argv[1:])

inputfile = '/home/dooky/Desarrollo/FEDECOBA/Archivos Consumos/lecturas_prueba.txt'
outputfile = '/home/dooky/Desarrollo/FEDECOBA/Archivos Consumos/lecturas_estandar.txt'
convertir(inputfile, outputfile)