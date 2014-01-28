#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Rango']


class Rango(ModelSQL, ModelView):
    "Rango"
    __name__ = 'sigcoop_usuario.rango'
    #minimo y maximo de rango de acciones asignadas
    minimo = fields.Integer('Minimo', required=True)
    maximo = fields.Integer('Maximo', required=True)
    #Referencia asociados
    asociado = fields.Many2One('party.party', 'Asociado', domain=[('asociado', '=', True)])
