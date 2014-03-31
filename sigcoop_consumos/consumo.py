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
    fecha = fields.Date('Fecha lec. actual', required=True)
    lectura = fields.BigInteger('Lectura actual', required=True)
    consumo_neto = fields.BigInteger('Consumo Neto', required=True)
    


#----------------------------Wizard de importacion----------------------------------#

class ImportacionStart(ModelView): 
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
            (suministro,_,resto) = linea.partition(',')
            (medidor,_,resto) = resto.partition(',')
            (period,_,resto) = resto.partition(',')
            (fecha,_,resto) = resto.partition(',')
            (estado,_,consumoNeto) = resto.partition(',')


            consumo_t = Pool().get('sigcoop_consumos.consumo')
            suministro_t = Pool().get('sigcoop_usuario.suministro')
            try:
                existe_suministro = suministro_t(suministro_t.search([('codigo_suministro', '=', suministro)])[0])
                consumo_nuevo = consumo_t.create([{
                        'id_suministro':existe_suministro.id,
                        'id_medidor':medidor,
                        'periodo':period,
                        'fecha':date,
                        'lectura':estado,
                        'consumo_neto':c_neto,
                    }])[0]
                consumo_nuevo.save()
            except:
                print 'El suministro ', suministro, ' no existe.'
        return 'end'



