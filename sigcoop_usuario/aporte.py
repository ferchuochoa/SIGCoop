#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Aporte']


class Aporte(ModelSQL, ModelView):
    "Aporte"
    __name__ = 'sigcoop_usuario.aporte'
    fecha = fields.Date('Fecha')
    monto = fields.Integer('Monto')
    sector = fields.Many2One('account_sector.sector', 'Sector')
    usuario_id = fields.Many2One('party.party', 'Usuario', domain=[('asociado', '=', True)])
