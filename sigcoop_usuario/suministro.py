#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Suministro']


class Suministro(ModelSQL, ModelView):
    "Suministro"
    __name__ = 'sigcoop_usuario.suministro'
    usuario_id = fields.Many2One('party.party', 'Usuario')
    numero_suministro = fields.Integer('Numero suministro')
    servicio = fields.Selection(
        [
            ('luz', 'Luz'),
            ('agua', 'Agua'),
            # TODO: Completar servicios.
        ],
        'Tipo de servicio'
    )
    ruta = fields.Integer('Ruta')
    calle = fields.Char('Calle')
    calle_numero = fields.Char('Numero')
