#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Medidor']


class Medidor(ModelSQL, ModelView):
    "Medidor"
    __name__ = 'sigcoop_suministro.medidor'
    consumos = fields.One2Many('sigcoop_consumos.consumo', 'id_medidor', 'Consumos')