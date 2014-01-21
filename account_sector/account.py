#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Account', 'Sector']

class Account(ModelSQL, ModelView):
    "Account"
    __name__ = 'account.account'
    sector_id = fields.Many2One('account_sector.sector', 'Sector', required=False)

class Sector(ModelSQL, ModelView):
    "Sector"
    __name__ = 'account_sector.sector'
    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account', 'sector_id', 'Cuentas', required=False)
