from datetime import date
import csv
import zipfile

'''
Archivo Refresh
---------------

Nombre del archivo nomeclatura: PEEEVMDD
P: Fijo
EEE: Codigo Ente asignado x RedLink (123)
V: Identificacion numerica consecutiva del volumen
M: Identificacionn del mes (mes 10 es A, mes 11 es B y mes 12 C)
DD: Indetificaion del dia 
'''
RF_P = "P"
RF_EEE = str(999)
RF_V = str(1) 
RF_M = str(3)
RF_DD = str(date.today().day)
RF_EXT = "csv"
refresh_file = RF_P+RF_EEE+RF_V+RF_M+RF_DD+"."+RF_EXT #"P9991321.csv"
 
'''
Archivo Control
---------------

Nombre del archivo nomeclatura: CEEE1MDD
C: Fijo
EEE: Codigo Ente asignado x RedLink (123)
1: Nro del volumen (de 0 a 9 en el caso q se envie mas de un archivo fisico)
M: Identificacion del mes (va de 1 a 9 y de A a C)
DD: Nro del dia de 01 a 31 (menores a 10 se agrego cero agrega a izquierda) 
'''
CTRL_C = "C"
CTRL_EEE = str(999)
CTRL_1 = str(1)
CTRL_M = str(date.today().month)
CTRL_EXT = "csv"
control_refresh_file = CTRL_C+CTRL_EEE+CTRL_1+CTRL_M+"."+CTRL_EXT #"C1230321.csv"

facturas_apagar = [['Fernanda Ochoa', '25/03/2014', 100],
                   ['Martin Di Lisio', '22/03/2014', 200],
                   ['Ezequiel Fernandez Vera', '28/03/2014', 540]]


def create_zip_file(name_file):
	# Create zip file
	f = zipfile.ZipFile(name_file+'.zip', 'w')
	f.write('file1.txt')
	# flush and close
	f.close()

def add_header_refresh(wr_refresh):
	'''
	----------------------------------------------------------------------------------------------------------
	| Posicion | Longitud | Formato | Descripcion      |        Contenido   	 							 |
	|          |          |         |                  |        		    	 							 |
	| 1 -  13  |   13     |         | Identificacion   | Fijo: HRFACTURACION	 							 |
	| 14 - 16  |    3     |   AN    | Codigo Ente      | Asignado por Red Link	 							 |
	| 17 - 22  |    6     |    N    | Fecha de proceso | AA MM DD          		 							 |
	| 23 - 27  |    5     |    N    | Lote             | Numero que identifica cada uno de los N lotes q se  |
	|          |          |         |                  | incluyen en el archivo.          				     |
	| 28 - 131 |   104    |         | Filler           | Espacios ( completar hasta llegar a la misma        |
	|		   |		  |			|				   | longitud que el registro de datos )          		 |
	|          |          |         |                  |           				                             |
	----------------------------------------------------------------------------------------------------------
	'''

	wr_refresh.writerow(['Inicial Refresh'])

def add_refresh_reg_datos(wr_refresh, datos):
	'''
	------------------------------------------------------------------------------------------------------------------
	| Posicion | Longitud | Formato | Descripcion               |                 Contenido   	 					 |
	|          |          |         |                           |        		    	 						 	 |
	| 1 -  5   |    5     |    N    | Identificacion de deuda   | Nro. Acordado (RedLink & Ente)				 	 |
	| 6 -  8   |    3     |    N    |(Completar con ceros a izq)|                                              		 |
	|          | 		  |         |Id. de concepto            | Nro. Acordado (RedLink & Ente) Identificador 		 |
	|          |          |         |                           | de los conceptos a cobrar.                   		 |
	| 9 - 27   |    19    |    N    |(Completar con espacios a  | Codigo identifica a titulares de las obligaciones. |
	|          |          |         |derecha) Id. Usuario       | Min. 7 posiciones, Max 19. 						 |
	| 28 - 33  |    6     |    N    | Fecha 1er Vencimiento     | AA MM DD                                           |
	| 34 - 45  |  10 + 2  |    N    |(Completar con ceros a izq)|                                   				 |
	|          |          |         |Importe 1er Vencimiento.   |													 |	 
	| 46 - 51  |    6     |    N    | Fecha 2do Vencimiento     | AA MM DD si no se usa completar con Ceros          |
	| 52 - 63  |  10 + 2  |	   N	|(Completar con ceros a izq)| si no se usa completar con Ceros                   |
	|          |          |         |Importe 2do Vencimiento.   |          				                             |
	| 64 - 69  |    6     |    N    | Fecha 3er Vencimiento.    | AA MM DD si no se usa completar con Ceros          |
	| 70 - 81  |  10 + 2  |    N    |(Completar con ceros a izq)| si no se usa completar con Ceros   				 |
	|          |          |         |Importe 3er Vencimiento.   |													 |	 
	| 82 - 131 |    50    |   AN    | Discrecional              | Posiciones libre para incorporar datos             |
	------------------------------------------------------------------------------------------------------------------
	'''

	wr_refresh.writerows(datos)


def add_trailer_refresh(wr_refresh):
	'''
	----------------------------------------------------------------------------------------------------------
	| Posicion | Longitud | Formato | Descripcion      |        Contenido   	 							 |
	|          |          |         |                  |        		    	 							 |
	| 1 -  13  |   13     |         | Identificacion   | Fijo: HRFACTURACION	 							 |
	| 14 - 21  |    8     |    N    | Cantidad de reg. | Incluyendo inicial y final 						 |
	| 22 - 39  | 16 + 2   |    N    | Total 1er Venc.  | Suma de todos los importes. Completar con 0 a izq.	 |
	| 40 - 57  | 16 + 2   |    N    | Total 2do Venc.  | Suma de todos los importes. Completar con 0 a izq.  |
	| 58 - 75  | 16 + 2   |    N    | Total 3er Venc.  | Suma de todos los importes. Completar con 0 a izq.  |
	| 76 - 131 |   55	  |			| Filler		   | Espacios. Completar hasta llegar a la misma long.   |
	|          |          |         |                  | que el registro de datos.                           |
	----------------------------------------------------------------------------------------------------------
	'''
	wr_refresh.writerow(['Final Refresh'])


def add_control_reg_inicial(wr_control):
	'''
	----------------------------------------------------------------------------------------------------------
	| Posicion | Longitud | Formato | Descripcion              |             Contenido						 |
	|          |          |         |                          |        		    						 |
	| 1 -  9   |    9     |    X    | Identificacion de inicio | Fijo: HRPASCTRL							 |
	| 10 - 17  |    8     |    9    | Fecha                    | AAAAMMDD   	 							 |
	| 18 - 20  |    3     |    X    | Ente                     | Codigo de RedLink 							 |
	| 21 - 28  |    8     |    X    | Nombre Archivo           | Nombre del archivo refresh (ej. P0141727)   |
	| 29 - 38  |    10    |    9    | Longitud del Archivo     | Total de bytes del archivo/s refresh.  	 |
	|          |          |         |                          | Total = cant reg de refresh x long de reg.  |
	| 39 - 75  |    37    |    X    | Filler                   | Espacios ( completar fin de reg.)           |
	|          |          |         |        		           |   				                             |
	----------------------------------------------------------------------------------------------------------
	'''
	wr_control.writerow(['Inicial Control'])

def add_control_reg_datos(wr_control, datos):	
	'''
	----------------------------------------------------------------------------------------------------------
	| Posicion |  Formato | Descripcion              |             Contenido		        				 |
	|          |          |                          |        		    					            	 |
	| 1 -  5   |    X(5)  | Identificacion de datos  | Fijo: LOTES							                 |
	| 6 -  10  |    9(5)  | Numero de lote           | Identificacion numerica asignada al lote de refresh   |
	| 11 - 18  |    9(8)  | Cantidad de reg de lote  | Cantidad total de registros del lote                  |
	| 19 - 36  | 9(16)V99 | Importe 1er Vencimiento  | Suma de importes 1er vencimiento del lote. 0s izq     |
	| 37 - 54  | 9(16)V99 | Importe 2do Vencimiento  | Suma de importes 2do vencimiento del lote. 0s izq     |
	| 55 - 72  | 9(16)V99 | Importe 3er Vencimiento  | Suma de importes 2do vencimiento del lote. 0s izq     |
	| 73 - 75  |    3     | Filler  		         | Espacios  				                             |
	----------------------------------------------------------------------------------------------------------
	'''
	cantidad = len(datos)
	totales = 0
	for total in datos:
		totales += total[2]
	wr_control.writerow([cantidad, totales])

def add_control_reg_final(wr_control):
	'''
	----------------------------------------------------------------------------------------------------------
	| Posicion |  Formato | Descripcion              |             Contenido		        				 |
	|          |          |                          |        		    					            	 |
	| 1 -  5   |    X(5)  | Identificacion de fin    | "FINAL"							                     |
	| 6 -  13  |    9(8)  | Cantidad de reg de lote  | Cantidad total de registros del lote de refresh       |
	| 14 - 31  | 9(16)V99 | Importe Total 1er Venc   | Suma de importes 1er vencimiento del lote. 0s izq     |
	| 32 - 49  | 9(16)V99 | Importe Total 2do Venc   | Suma de importes 2do vencimiento del lote. 0s izq     |
	| 50 - 67  | 9(16)V99 | Importe Total 3er Venc   | Suma de importes 3do vencimiento del lote. 0s izq     |
	| 68 - 75  |    X(8)  | Fecha Ultimo Vencimiento | Fecha ultimo vencimiento     						 |
	----------------------------------------------------------------------------------------------------------
	'''
	wr_control.writerow(['Final Control'])



if __name__ == '__main__':
	#print RF_DD
	with open(refresh_file, 'w') as outputrefresh:
		wr_refresh = csv.writer(outputrefresh, quoting=csv.QUOTE_ALL)
		add_header_refresh(wr_refresh)
		add_refresh_reg_datos(wr_refresh, facturas_apagar)
		add_trailer_refresh(wr_refresh)

	with open(control_refresh_file, 'w') as outputcontrol:
		wr_control = csv.writer(outputcontrol, quoting=csv.QUOTE_ALL)
		add_control_reg_inicial(wr_control)
		add_control_reg_datos(wr_control, facturas_apagar)
		add_control_reg_final(wr_control)
