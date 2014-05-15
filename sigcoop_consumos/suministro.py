#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Suministro']


class Suministro(ModelSQL, ModelView):
    "Suministro"
    __name__ = 'sigcoop_usuario.suministro'
    consumos = fields.One2Many('sigcoop_consumos.consumo', 'id_suministro', 'Consumos')