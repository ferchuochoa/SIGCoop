#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Suministro', 'SuministroMedidor']


class Suministro(ModelSQL, ModelView):
    "Suministro"
    __name__ = 'sigcoop_usuario.suministro'
    medidor = fields.One2One('sigcoop_usuario.suministro_medidor', 'suministro', 'medidor',
            string='Medidor', required=False)


class SuministroMedidor(ModelSQL):
    'Suministro Medidor'
    __name__= 'sigcoop_usuario.suministro_medidor'

    suminitro = fields.Many2One('sigcoop_usuario.suministro', 'Suministro')
    medidor = fields.Many2One('sigcoop_medidor.medidor', 'Medidor')

    @classmethod
    def __setup__(cls):
        super(SuministroMedidor, cls).__setup__()
        cls._sql_constraints += [
            ('suminitro_unique', 'UNIQUE(suminitro)',
                'suminitro must be unique'),
            ('medidor_unique', 'UNIQUE(medidor)',
                'medidor must be unique'),
            ]