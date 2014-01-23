#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond import backend

__all__ = ['SectorTemplate', 'Sector', 'AccountTemplate',  'Account', 'CreateChartAccount', 'CreateChart']


class SectorTemplate(ModelSQL, ModelView):
    "Sector Template"
    __name__ = 'account.sector.template'
    name = fields.Char('Nombre', required=True)
    cuentas = fields.One2Many('account.account.template', 'sector_id', 'Cuentas')
   

    @classmethod
    def __setup__(cls):
        super(SectorTemplate, cls).__setup__()


    def create_sector(self, template2sector=None):
        '''
        Create recursively types based on template.
        template2type is a dictionary with template id as key and type id as
        value, used to convert template id into type. The dictionary is filled
        with new types.
        Return the id of the type created
        '''
        pool = Pool()
        Sector = pool.get('account.sector')
        Config = pool.get('ir.configuration')

        if template2sector is None:
            template2sector = {}

        if self.id not in template2sector:
            vals['name'] = self.name

            new_sector, = Sector.create([vals])

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
                    for field_name, field in template._fields.iteritems():
                        if (getattr(field, 'translate', False)
                                and (getattr(template, field_name) !=
                                    prev_data[field_name])):
                            data[field_name] = getattr(template, field_name)
                    if data:
                        Sector.write([new_sector], data)
            template2sector[self.id] = new_sector.id
        new_id = template2sector[self.id]

        new_childs = []
        for child in self.childs:
            new_childs.append(child.create_sector(template2sector=template2sector))
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

        if self.id not in template2account:
            vals = self._get_account_value()
            vals['company'] = company_id + "2"
            vals['parent'] = parent_id
            vals['type'] = (template2type.get(self.type.id) if self.type
                else None)
         #   vals['sector_id'] = (template2sector.get(self.sector_id.id))

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


class CreateChartAccount(ModelView):
    'Create Chart'
    __name__ = 'account.create_chart.account'
    account_template = fields.Many2One('account.account.template',
            'Account Template', required=True, domain=[('parent', '=', None)])

    

class CreateChart(Wizard):
    'Create Chart'
    __name__ = 'account.create_chart'

    account = StateView('account.create_chart.account',
        'account.create_chart_account_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create', 'create_account', 'tryton-ok', default=True),
            ])

    def transition_create_account(self):
        pool = Pool()
        TaxCodeTemplate = pool.get('account.tax.code.template')
        TaxTemplate = pool.get('account.tax.template')
        TaxRuleTemplate = pool.get('account.tax.rule.template')
        TaxRuleLineTemplate = \
            pool.get('account.tax.rule.line.template')
        Config = pool.get('ir.configuration')

        with Transaction().set_context(language=Config.get_language(),
                company=self.account.company.id):
            account_template = self.account.account_template

            # Create account sectores
            template2sector = {}
            account_template.sector_id.create_sector(template2sector=template2sector)


            # Create account types
            template2type = {}
            account_template.type.create_type(self.account.company.id,
                template2type=template2type)

            # Create accounts
            template2account = {}
            account_template.create_account(self.account.company.id,
                template2account=template2account, template2type=template2type, template2sector=template2sector)



            # Create tax codes
            template2tax_code = {}
            tax_code_templates = TaxCodeTemplate.search([
                    ('account', '=', account_template.id),
                    ('parent', '=', None),
                    ])
            for tax_code_template in tax_code_templates:
                tax_code_template.create_tax_code(self.account.company.id,
                    template2tax_code=template2tax_code)

            # Create taxes
            template2tax = {}
            tax_templates = TaxTemplate.search([
                    ('account', '=', account_template.id),
                    ('parent', '=', None),
                    ])
            for tax_template in tax_templates:
                tax_template.create_tax(self.account.company.id,
                    template2tax_code=template2tax_code,
                    template2account=template2account,
                    template2tax=template2tax)

            # Update taxes on accounts
            account_template.update_account_taxes(template2account,
                template2tax)

            # Create tax rules
            template2rule = {}
            tax_rule_templates = TaxRuleTemplate.search([
                    ('account', '=', account_template.id),
                    ])
            for tax_rule_template in tax_rule_templates:
                tax_rule_template.create_rule(self.account.company.id,
                    template2rule=template2rule)

            # Create tax rule lines
            template2rule_line = {}
            tax_rule_line_templates = TaxRuleLineTemplate.search([
                    ('rule.account', '=', account_template.id),
                    ])
            for tax_rule_line_template in tax_rule_line_templates:
                tax_rule_line_template.create_rule_line(template2tax,
                    template2rule, template2rule_line=template2rule_line)
        return 'properties'
