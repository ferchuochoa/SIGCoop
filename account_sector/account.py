#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Account', 'Sector', 'AccountTemplate', 'SectorTemplate']


class SectorTemplate(ModelSQL, ModelView):
    "Sector Template"
    __name__ = 'account_sector.sector.template'
    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account.template', 'sector_id', 'Cuentas', required=False)

class Sector(ModelSQL, ModelView):
    "Sector"
    __name__ = 'account_sector.sector'
    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account', 'sector_id', 'Cuentas', required=False)
    template = fields.Many2One('account_sector.sector.template', 'Template')


class AccountTemplate(ModelSQL, ModelView):
    'Account Template'
    __name__ = 'account.account.template'
    sector_id = fields.Many2One('account_sector.sector.template', 'Sector', ondelete="RESTRICT", required=False)


class Account(ModelSQL, ModelView):
    "Account"
    __name__ = 'account.account'
    sector_id = fields.Many2One('account_sector.sector', 'Sector', ondelete="RESTRICT", required=False)
