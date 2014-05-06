#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import In, Eval

__all__ = ['Suministro']

TARIFAS = [
("T1AP", "T1AP Alumbrado Publico"),
("T1GAC", "T1GAC Servicio General Alto Consumo"),
("T1GBC", "T1GBC Servicio General Bajo Consumo"),
("T1R", "T1R Residencial"),
("T1R2", "T1R Residencial Social"),
("T2BT", "T2BT Baja Tension"),
("T2MT", "T2MT Media Tension"),
("T3BT", "T3BT Baja Tension (>300KW)"),
("T3BT2", "T3BT Baja Tension (50 a 300KW)"),
("T3MT", "T3MT Media Tension (>300KW)"),
("T3MT2", "T3MT Media Tension (50 a 300KW)"),
("T4", "T4 Rural"),
("T5BT", "T5BT Baja Tension (>300KW)"),
("T5BT2", "T5BT Baja Tension (50 a 300KW)"),
("T5MT", "T5MT Media Tension (>300KW)"),
("T5MT2", "T5MT Media Tension (50 a 300KW)"),
]

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
