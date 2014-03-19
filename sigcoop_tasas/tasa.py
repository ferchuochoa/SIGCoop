#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Tasa']

class Tasa(ModelSQL, ModelView):
    "Tasa"
    __name__ = 'sigcoop_tasas.tasa'
    desde = fields.Date('Desde')
    valor = fields.Float('Valor')
    tipo = fields.Selection(
        [
            ('banco', 'Banco'),
            ('cooperativa', 'Cooperativa'),
        ],
        'Tipo de tasa'
    )
