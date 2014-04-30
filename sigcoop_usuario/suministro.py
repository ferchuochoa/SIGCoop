#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Suministro']


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
