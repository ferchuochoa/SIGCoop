#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from datetime import *


class Consumo(ModelSQL, ModelView):
    "Consumo"
    __name__ = 'sigcoop_consumos.consumo'

    id_suministro = fields.Many2One('sigcoop_usuario.suministro', 'Suministro', required=True)
    id_medidor = fields.Many2One('sigcoop_medidor.medidor', 'Medidor', required=True)
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


    @classmethod
    def __setup__(cls):
        super(Consumo, cls).__setup__()
        cls._sql_constraints += [
            ('consumo_pk', 'UNIQUE(id_suministro, id_medidor, periodo, concepto)',
                'No puede haber mas de un consumo para el mismo medidor en un periodo y para un concepto'),
            ]


#----------------------------Wizard de importacion----------------------------------#

class ImportacionStart(ModelView): 
    "Importacion Start"
    __name__= 'sigcoop_consumos.importacion_consumos.start'

    file = fields.Binary('Archivo')
    periodo = fields.Char('Periodo', required=True)
    checkListado = fields.Boolean('Hacer listado')


class ImportacionResumen(ModelView):
    "Importacion Resumen"
    __name__= 'sigcoop_consumos.importacion_consumos.resumen'

    resumen = fields.Text('Resumen de importacion', readonly = True)


    elDato = 'algo'

    def get_dato(self):
        print self.elDato + ' get'
        return self.elDato

    def set_dato(self, dato):
        self.elDato = dato
        print self.elDato + ' set'

    @classmethod
    def default_resumen(cls):
        return 'hola' + cls.elDato


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

            (dia,_,resto) = fecha.partition('-')
            (mes,_,anio) = resto.partition('-')
            fechaActual = date(int(anio),int(mes),int(dia))


            consumo_t = Pool().get('sigcoop_consumos.consumo')
            suministro_t = Pool().get('sigcoop_usuario.suministro')
            medidor_t = Pool().get('sigcoop_medidor.medidor')
            try:
                existe_suministro = suministro_t(suministro_t.search([('codigo_suministro', '=', suministro)])[0])
                try:
                    existe_medidor = medidor_t(medidor_t.search(['id_medidor', '=', medidor])[0])
                    print 'sum: ', existe_suministro.id, 'med: ', existe_medidor.id, 'per: ', period, 'con: ', concept, 'fecha: ', fechaActual, 'estado: ', estado, 'c neto: ', consumoNeto
                    consumo_nuevo = consumo_t.create([{
                            'id_suministro':existe_suministro.id,
                            'id_medidor':existe_medidor.id,
                            'periodo':period,
                            'concepto':concept,
                            'fecha':fechaActual,
                            'lectura':estado,
                            'consumo_neto':int(consumoNeto)* existe_medidor.registrador,
                        }])[0]
                    consumo_nuevo.save()
                except:
                    print 'El medidor ', medidor, ' no exite.'
            except:
                print 'El suministro ', suministro, ' no existe.'


        # if self.start.checkListado:
        # #     generarListadoConsistencia()
        self.resumen.set_dato('el dato que paso')
        return 'resumen'



    def generarListadoConsistencia(self):
        pass
