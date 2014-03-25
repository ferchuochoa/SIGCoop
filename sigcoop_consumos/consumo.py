#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from datetime import *


class Consumo(ModelSQL, ModelView):
    "Consumo"
    __name__ = 'sigcoop_consumos.consumo'

    id_suministro = fields.Many2One('sigcoop_usuario.suministro', 'Suministro', required=True)
    id_medidor = fields.Char('Medidor', required=True)
    periodo = fields.Char('Periodo', required=True)
    fecha_anterior = fields.Date('Fecha lec. anterior', required=True)
    lectura_anterior = fields.BigInteger('Lectura anterior', required=True)
    fecha_actual = fields.Date('Fecha lec. actual', required=True)
    lectura_actual = fields.BigInteger('Lectura actual', required=True)
    consumo_neto = fields.BigInteger('Consumo Neto', required=True)


#----------------------------Wizard de importacion----------------------------------#

class ImportacionStart(ModelView): #no agrego el ModelSQL porque no quiero crear la tabla en la BD, solo quiero una vista
    "Importacion Start"
    __name__= 'sigcoop_consumos.importacion_consumos.start'
    file = fields.Binary('Archivo')


class ImportacionConsumos(Wizard):
    "Importacion Consumos"
    __name__= 'sigcoop_consumos.importacion_consumos'

    start = StateView('sigcoop_consumos.importacion_consumos.start', 'sigcoop_consumos.view_importacion_form', 
                      [Button('Cancelar', 'end', 'tryton-cancel'), 
                       Button('Importar', 'importar', 'tryton-go-next', default = True)])

    importar = StateTransition()

    def transition_importar(self):
        #obtengo el esquema de consumo
        consumo_t = Pool().get('sigcoop_consumos.consumo')
        #obtengo el archivo del campo file del modelo relacionado con el estado "start"
        file = self.start.file
        i = 0
        while (i < len(file)):
            linea = ''
            while (i < len(file)) and (not file[i] == '\n'):
                linea += file[i]
                i+= 1 
            i+= 1
            (calle,_,resto) = linea.partition(':')
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
            c_anterior = long(consumo_anterior)
            c_actual = long(consumo_actual)
            c_neto = c_actual - c_anterior

            # print 'CONSUMOS: c_anterior ', c_anterior, ', c_actual ', c_actual, ', c_neto', c_neto
            # print 'FECHAS: f_actual: ', f_actual, ', f_anterior: ', f_anterior, ', period: ', period


            consumo_t = Pool().get('sigcoop_consumos.consumo')
            suministro_t = Pool().get('sigcoop_usuario.suministro')
            try:
                existe_suministro = suministro_t(suministro_t.search([('codigo_suministro', '=', suministro)])[0])
                consumo_nuevo = consumo_t.create([{
                        'id_suministro':existe_suministro.id,
                        'id_medidor':medidor,
                        'periodo':period,
                        'fecha_anterior':f_anterior,
                        'lectura_anterior':c_anterior,
                        'fecha_actual':f_actual,
                        'lectura_actual':c_actual,
                        'consumo_neto':c_neto,
                    }])[0]
                consumo_nuevo.save()
            except:
                print 'El suminitro ', suministro, ' no existe.'
        return 'end'



