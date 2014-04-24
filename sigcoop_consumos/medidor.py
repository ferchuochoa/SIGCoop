#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Medidor']


class Medidor(ModelSQL, ModelView):
    "Medidor"
    __name__ = 'sigcoop_consumos.medidor'

    idMedidor = fields.Char('IdMedidor', required=True)
    registrador = fields.Integer('Registrador', required=True)
    consumos = fields.One2Many('sigcoop_consumos.comsumo', 'id_medidor', 'Consumos')

    @staticmethod
    def default_registrador():
        return 1
