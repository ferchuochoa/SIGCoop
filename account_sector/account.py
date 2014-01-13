#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Account', 'Sector']

class Account(ModelSQL, ModelView):
    "Account"
    __name__ = 'account.account'
    sector_id = fields.Many2One('account_sector.sector', 'sector', required=False)

class Sector(ModelSQL, ModelView):
    "Sector"
    __name__ = 'account_sector.sector'
    name = fields.Char('nombre2', required=True)
    cuentas = fields.One2Many('account.account', 'sector_id', 'cuentas', required=False)
