#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Party']


class Party(ModelSQL, ModelView):
    "Party"
    __name__ = 'party.party'
    #El field asociado nos da a elegir si es asociado o cliente.
    #Por defecto, es cliente ya que el campo es false.
    asociado = fields.Boolean('Es Asociado')
    dir_entrega_factura = fields.Many2One('party.address', 'Direccion entrega factura')
    ruta = fields.Integer('Ruta')
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
    valor_identificacion = fields.Integer('Valor identificacion')
    #El numero indica el numero de cliente o
    #asociado segun se indique en el campo asociado.
    numero = fields.Integer('Numero de Cliente/Asociado')
    numero_titulo = fields.Integer('Numero de titulo')
    fecha_ingreso = fields.Date('Fecha de ingreso')
    #Referencias muchos a uno
    suministros = fields.One2Many('sigcoop_usuario.suministro', 'usuario_id', 'Suministros')
