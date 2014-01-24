#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Familiar']


class Familiar(ModelSQL, ModelView):
    "Familiar"
    __name__ = 'sigcoop_usuario.familiar'
    dni = fields.Integer('Dni', required=True)
    relacion = fields.Selection(
        [
            ('hijo', 'Hijo'),
            ('conyuge', 'Conyuge'),
        ],
        'Relacion'
    )
    nombre = fields.Char('Nombre')
    apellido = fields.Char('Apellido')
    fecha_nacimiento = fields.Date('Fecha de nacimiento')
    #Referencia a un party del tipo asociado. El domain filtra por asociados en el form de creacion.
    usuario_id = fields.Many2One('party.party', 'Usuario', domain=[('asociado', '=', True)])
