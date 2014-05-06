#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Medidor']


class Medidor(ModelSQL, ModelView):
    "Medidor"
    __name__='sigcoop_medidor.medidor'

    id_medidor = fields.Char('Medidor', required = True)
    registrador = fields.Integer('Registrador', required = True)