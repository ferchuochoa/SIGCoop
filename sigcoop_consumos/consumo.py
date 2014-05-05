#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from datetime import *


class Consumo(ModelSQL, ModelView):
    "Consumo"
    __name__ = 'sigcoop_consumos.consumo'

    id_suministro = fields.Many2One('sigcoop_usuario.suministro', 'Suministro', required=True)
    id_medidor = fields.Many2One('sigcoop_suministro.medidor', 'Medidor', required=True)
    # id_medidor = fields.Char('Medidor', required = True)
    periodo = fields.Char('Periodo', required=True)
    concepto =  fields.Selection(
        [
            ('1', 'Cargo variable'),
            ('2', 'Cargo variable Pico'),
            ('3', 'Cargo variable Fuera de pico'),
            ('4', 'Cargo variable Valle'),
            ('5', 'Cargo variable Resto'),
            ('6', 'Potencia Pico'),
            ('7', 'Potencia Resto'),
            ('8', 'Exceso potencia Pico'),
            ('9', 'Exceso potencia Resto'),
            ('10', 'Cargo perdida Transformador'),
            ('11', 'Recargos x Bajo Cos Fi'),
        ],
        'Concepto'
    )
    fecha = fields.Date('Fecha lec. actual', required=True)
    lectura = fields.BigInteger('Lectura actual', required=True)
    consumo_neto = fields.BigInteger('Consumo Neto', required=True)
    estado = fields.Selection(
        [
            ('0', 'No facturable'),
            ('1', 'Facturable'), 
            ('2', 'Facturado'),
        ],
        'Estado'
    )


#----------------------------Wizard de importacion----------------------------------#

class ImportacionStart(ModelView): 
    "Importacion Start"
    __name__= 'sigcoop_consumos.importacion_consumos.start'

    file = fields.Binary('Archivo')
    periodo = fields.Char('Periodo')
    checkListado = fields.Boolean('Hacer listado')


class ImportacionResumen(ModelView):
    "Importacion Resumen"
    __name__= 'sigcoop_consumos.importacion_consumos.resumen'

    resumen = fields.Text('Resumen de importacion', readonly = True)

    dato = fields.Function(fields.Char('Un dato'), 'get_dato')

    elDato = ''

    def get_dato(self):
        print self.elDato + ' get'
        return self.elDato

    def set_dato(self, dato):
        self.elDato = dato
        print self.elDato + ' set'

    @classmethod
    def default_resumen(cls):
        return 'hola'


class ImportacionConsumos(Wizard):
    "Importacion Consumos"
    __name__= 'sigcoop_consumos.importacion_consumos'

    start = StateView('sigcoop_consumos.importacion_consumos.start', 'sigcoop_consumos.view_importacion_form', 
                      [Button('Cancelar', 'end', 'tryton-cancel'), 
                       Button('Importar', 'importar', 'tryton-go-next', default = True)])

    importar = StateTransition()

    resumen = StateView('sigcoop_consumos.importacion_consumos.resumen', 'sigcoop_consumos.view_importacion_resumen_form',
                        [ Button('Fin', 'end', 'tryton-ok', default = True)])

    def transition_importar(self):
        #obtengo el esquema de consumo
        consumo_t = Pool().get('sigcoop_consumos.consumo')
        #obtengo el archivo del campo file del modelo relacionado con el estado "start"
        file = self.start.file
        period = self.start.periodo
        i = 0
        while (i < len(file)):
            linea = ''
            while (i < len(file)) and (not file[i] == '\n'):
                linea += file[i]
                i+= 1 
            i+= 1
            (suministro,_,resto) = linea.partition(',')
            (medidor,_,resto) = resto.partition(',')
            (concept,_,resto) = resto.partition(',')
            (fecha,_,resto) = resto.partition(',')
            (estado,_,consumoNeto) = resto.partition(',')


            consumo_t = Pool().get('sigcoop_consumos.consumo')
            suministro_t = Pool().get('sigcoop_usuario.suministro')
            # medidor_t = Pool().get('sigcoop_consumos.medidor')
            try:
                existe_suministro = suministro_t(suministro_t.search([('codigo_suministro', '=', suministro)])[0])
                # existe_medidor = medidor_t(medidor_t.search(['idMedidor', '=', medidor])[0])
                consumo_nuevo = consumo_t.create([{
                        'id_suministro':existe_suministro.id,
                        'id_medidor':medidor,
                        'periodo':period,
                        'concepto':concept,
                        'fecha':date,
                        'lectura':estado,
                        'consumo_neto':c_neto,
                    }])[0]
                consumo_nuevo.save()
            except:
                print 'El suministro ', suministro, ' no existe.'


        # if self.start.checkListado:
        #     generarListadoConsistencia()
        self.resumen.set_dato('el dato que paso')
        return 'resumen'



    def generarListadoConsistencia(self):
        pass
