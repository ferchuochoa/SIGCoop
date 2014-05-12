#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Medidor']


class Medidor(ModelSQL, ModelView):
    "Medidor"
    __name__='sigcoop_medidor.medidor'

    name = fields.Char('Medidor', required = True)
    registrador = fields.Integer('Registrador', required = True)


    @staticmethod
    def default_registrador():
        return 1
