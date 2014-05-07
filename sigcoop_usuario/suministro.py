#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import In, Eval

__all__ = ['Suministro']

TARIFAS_POTENCIA_KEYS = ['T2BT', 'T2MT', 'T3BT', 'T3BT2', 'T3MT', 'T3MT2', 'T5BT', 'T5BT2', 'T5MT', 'T5MT2']

class Suministro(ModelSQL, ModelView):
    "Suministro"
    __name__ = 'sigcoop_usuario.suministro'
    usuario_id = fields.Many2One('party.party', 'Usuario')
    codigo_suministro = fields.Char('Codigo suministro')
    servicio = fields.Selection(
        [
            ('luz', 'Luz'),
            ('agua', 'Agua'),
            ('gas', 'Gas'),
            # TODO: Completar servicios.
        ],
        'Tipo de servicio'
    )
    ruta = fields.Integer('Ruta')
    calle = fields.Char('Calle')
    calle_numero = fields.Char('Numero')
    #El tipo de alumbrado publico que se le cobra al cliente.
    impuesto_alumbrado = fields.Many2One('account.tax', 'Impuesto alumbrado publico')
    lista_precios = fields.Many2One('product.price_list', 'Lista de precios para tarifa')
    impuesto_alumbrado = fields.Many2One('account.tax', 'Impuesto alumbrado publico', domain=[('group.name', '=', 'Alumbrado')])
    lista_precios = fields.Many2One('product.price_list', 'Tarifa')
    potencia_contratada = fields.Integer('Potencia Contratada',
        states={
            'invisible': (~In(Eval('lista_precios'), TARIFAS_POTENCIA_KEYS))
        }
    )
