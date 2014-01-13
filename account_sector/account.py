__all__ = ['Account', 'Sector']

class Account(ModelSQL, ModelView):
    __name__ = 'account.account'
    sector_id = fields.Many2One('account_sector.sector', 'sector', required=False)

class Sector(ModelSQL, ModelView):
    __name__ = 'account_sector.sector'
    name = fields.Char('nombre', required=True)
    cuentas = fields.One2Many('account.account', 'sector_id', 'cuentas', required=True)
