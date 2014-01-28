#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond import backend


__all__ = ['SectorTemplate', 'Sector', 'AccountTemplate',  'Account']


class SectorTemplate(ModelSQL, ModelView):
    "Sector Template"
    __name__ = 'account.sector.template'
    
    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account.template', 'sector_id', 'Cuentas')
   

    @classmethod
    def __setup__(cls):
        super(SectorTemplate, cls).__setup__()


    def create_sector(self, template2sector=None):
        pool = Pool()
        Sector = pool.get('account.sector')

        if template2sector is None:
            template2sector = {}

        if self.id not in template2sector:
            vals = {}
            vals['name'] = self.name
            new_sector, = Sector.create([vals])
            template2sector[self.id] = new_sector.id

        new_id = template2sector[self.id]

        return new_id



class Sector(ModelSQL, ModelView):
    "Sector"
    __name__ = 'account.sector'

    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account', 'sector_id', 'Cuentas')
    template = fields.Many2One('account.sector.template', 'Template')


class AccountTemplate(ModelSQL, ModelView):
    'Account Template'
    __name__ = 'account.account.template'

    sector_id = fields.Many2One('account.sector.template', 'Sector',
            ondelete="RESTRICT")
 
    # @staticmethod
    # def default_sector_id():
    #     return 1

    def create_account(self, company_id, template2account=None,
            template2type=None, template2sector=None, parent_id=None):
        '''
        Create recursively accounts based on template.
        template2account is a dictionary with template id as key and account id
        as value, used to convert template id into account. The dictionary is
        filled with new accounts
        template2type is a dictionary with type template id as key and type id
        as value, used to convert type template id into type.
        Return the id of the account created
        '''
        pool = Pool()
        Account = pool.get('account.account')
        Lang = pool.get('ir.lang')
        Config = pool.get('ir.configuration')

        if template2account is None:
            template2account = {}

        if template2type is None:
            template2type = {}

        if template2sector is None:
            template2sector = {}

        if self.id not in template2account:
            vals = self._get_account_value()
            vals['company'] = company_id
            vals['parent'] = parent_id
            vals['type'] = (template2type.get(self.type.id) if self.type
                else None)
            if self.sector_id:
                self.sector_id.create_sector(template2sector)
                vals['sector_id'] = (template2sector.get(self.sector_id.id))
            else:
                vals['sector_id'] = None

            new_account, = Account.create([vals])

            prev_lang = self._context.get('language') or Config.get_language()
            prev_data = {}
            for field_name, field in self._fields.iteritems():
                if getattr(field, 'translate', False):
                    prev_data[field_name] = getattr(self, field_name)
            for lang in Lang.get_translatable_languages():
                if lang == prev_lang:
                    continue
                with Transaction().set_context(language=lang):
                    template = self.__class__(self.id)
                    data = {}
                    for field_name, field in self._fields.iteritems():
                        if (getattr(field, 'translate', False)
                                and (getattr(template, field_name) !=
                                    prev_data[field_name])):
                            data[field_name] = getattr(template, field_name)
                    if data:
                        Account.write([new_account], data)
            template2account[self.id] = new_account.id
        new_id = template2account[self.id]

        new_childs = []
        for child in self.childs:
            new_childs.append(child.create_account(company_id,
                template2account=template2account, template2type=template2type, 
                template2sector=template2sector, parent_id=new_id))
        return new_id


class Account(ModelSQL, ModelView):
    "Account"
    __name__ = 'account.account'
    sector_id = fields.Many2One('account.sector', 'Sector',
            ondelete="RESTRICT")
