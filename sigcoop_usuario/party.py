#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Party']


class Party(ModelSQL, ModelView):
    "Party"
    __name__ = 'party.party'
    #El field asociado nos da a elegir si es asociado o cliente.
    #Por defecto, es cliente ya que el campo es false.
    asociado = fields.Boolean('asociado')
    dir_entrega_factura = fields.Many2One('party.address', 'Direccion entrega factura')
    ruta = fields.Integer('Ruta')
    razon_social = fields.Selection(
        [
            ('CUIT', 'CUIT'),
            ('CUIL', 'CUIL'),
            ('DNI', 'DNI'),
        ],
        'Razon social'
    )
    #Este es el valor de cuil, cuit o dni,
    #segun se seleccione en el selection.
    valor_razon_social = fields.Integer('Valor razon social')
    #El numero indica el numero de cliente o
    #asociado segun se indique en el campo asociado.
    numero = fields.Integer('Numero')
    numero_titulo = fields.Integer('Numero de titulo')
    fecha_ingreso = fields.Date('Fecha de ingreso')
