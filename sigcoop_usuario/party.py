#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, If
from datetime import *

__all__ = ['Party']


class Party(ModelSQL, ModelView):
    "Party"
    __name__ = 'party.party'
    # El cliente/socio puede estar exento de PUREE
    exento_PUREE = fields.Boolean('Exento PUREE', help = "Marcar si el usuario esta exento frente al PUREE")
    #El field cliente_socio aparece al lado del nombre de la entidad para definir si va a ser de este tipo.
    cliente_socio = fields.Boolean('Cliente/Socio', on_change=['cliente_socio'], help="Marcar si es un cliente de la cooperativa")
    #El field asociado nos da a elegir si es asociado o cliente.
    #Por defecto, es cliente ya que el campo es false.
    asociado = fields.Boolean('Es Asociado', 
                                states = {'readonly': ~Eval('cliente_socio', True)}, 
                                depends=['cliente_socio'],
                                help="Marcar si es un socio de la cooperativa (debe ser cliente tambien)")
    dir_entrega_factura = fields.Many2One('party.address', 'Direccion entrega factura')
    ruta = fields.Char('Ruta')
    tipo_identificacion = fields.Selection(
        [
            ('CUIT', 'CUIT'),
            ('CUIL', 'CUIL'),
            ('DNI', 'DNI'),
        ],
        'Tipo de identificacion'
    )
    #Este es el valor de cuil, cuit o dni,
    #segun se seleccione en el selection.
    valor_identificacion = fields.Char('Nro. Identificacion')
    #El numero indica el numero de cliente o
    #asociado segun se indique en el campo asociado.
    numero = fields.Char('Nro. de Cliente/Asociado', required=True)
    numero_titulo = fields.Char('Nro. de titulo')
    fecha_ingreso = fields.Date('Fecha de ingreso')
    #Referencias muchos a uno
    suministros = fields.One2Many('sigcoop_usuario.suministro', 'usuario_id', 'Suministros')
    rangos = fields.One2Many('sigcoop_usuario.rango', 'asociado', 'Rangos')
    familiares = fields.One2Many('sigcoop_usuario.familiar', 'usuario_id', 'Familiares')
    aportes = fields.One2Many('sigcoop_usuario.aporte', 'usuario_id', 'Aportes')


    @staticmethod
    def default_tipo_identificacion():
        return 'DNI'


    @staticmethod
    def default_fecha_ingreso():
        return datetime.today()


    @staticmethod
    def default_numero():
        return '-1'

    def on_change_cliente_socio(self):
        if self.cliente_socio:
            return {'numero':None}
        return {'numero':'-1'}


