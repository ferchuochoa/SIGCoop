from decimal import Decimal

from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pool import Pool

__all__ = ['Invoice', 'InvoiceLine']

class Invoice(Workflow, ModelSQL, ModelView):
    'Invoice'
    __name__ = 'account.invoice'

    def _on_change_lines_taxes(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        InvoiceTax = pool.get('account.invoice.tax')
        Account = pool.get('account.account')
        TaxCode = pool.get('account.tax.code')
        res = {
            'untaxed_amount': Decimal('0.0'),
            'tax_amount': Decimal('0.0'),
            'total_amount': Decimal('0.0'),
            'taxes': {},
            }
        computed_taxes = {}
        if self.lines:
            context = self.get_tax_context()
            for line in self.lines:
                if (line.type or 'line') != 'line':
                    continue
                res['untaxed_amount'] += line.amount or 0
                with Transaction().set_context(**context):
                    if (line.product and line.product.dont_multiply):
                        taxes = Tax.compute(line.taxes,
                        line.unit_price or Decimal('0.0'),
                        1.0)
                    else:
                        taxes = Tax.compute(line.taxes,
                        line.unit_price or Decimal('0.0'),
                        line.quantity or 0.0)
                for tax in taxes:
                    key, val = self._compute_tax(tax,
                        self.type or 'out_invoice')
                    if not key in computed_taxes:
                        computed_taxes[key] = val
                    else:
                        computed_taxes[key]['base'] += val['base']
                        computed_taxes[key]['amount'] += val['amount']
        if self.currency:
            for key in computed_taxes:
                for field in ('base', 'amount'):
                    computed_taxes[key][field] = self.currency.round(
                        computed_taxes[key][field])
        tax_keys = []
        for tax in (self.taxes or []):
            if tax.manual:
                res['tax_amount'] += tax.amount or Decimal('0.0')
                continue
            key = (tax.base_code.id if tax.base_code else None, tax.base_sign,
                tax.tax_code.id if tax.tax_code else None, tax.tax_sign,
                tax.account.id if tax.account else None,
                tax.tax.id if tax.tax else None)
            if (key not in computed_taxes) or (key in tax_keys):
                res['taxes'].setdefault('remove', [])
                res['taxes']['remove'].append(tax.id)
                continue
            tax_keys.append(key)
            if self.currency:
                if not self.currency.is_zero(
                        computed_taxes[key]['base']
                        - (tax.base or Decimal('0.0'))):
                    res['tax_amount'] += computed_taxes[key]['amount']
                    res['taxes'].setdefault('update', [])
                    res['taxes']['update'].append({
                            'id': tax.id,
                            'amount': computed_taxes[key]['amount'],
                            'base': computed_taxes[key]['base'],
                            })
                else:
                    res['tax_amount'] += tax.amount or Decimal('0.0')
            else:
                if (computed_taxes[key]['base'] - (tax.base or Decimal('0.0'))
                        != Decimal('0.0')):
                    res['tax_amount'] += computed_taxes[key]['amount']
                    res['taxes'].setdefault('update', [])
                    res['taxes']['update'].append({
                        'id': tax.id,
                        'amount': computed_taxes[key]['amount'],
                        'base': computed_taxes[key]['base'],
                        })
                else:
                    res['tax_amount'] += tax.amount or Decimal('0.0')
        for key in computed_taxes:
            if key not in tax_keys:
                res['tax_amount'] += computed_taxes[key]['amount']
                res['taxes'].setdefault('add', [])
                value = InvoiceTax.default_get(InvoiceTax._fields.keys())
                value.update(computed_taxes[key])
                for field, Target in (
                        ('account', Account),
                        ('base_code', TaxCode),
                        ('tax_code', TaxCode),
                        ('tax', Tax),
                        ):
                    if value.get(field):
                        value[field + '.rec_name'] = \
                            Target(value[field]).rec_name
                res['taxes']['add'].append(value)
        if self.currency:
            res['untaxed_amount'] = self.currency.round(res['untaxed_amount'])
            res['tax_amount'] = self.currency.round(res['tax_amount'])
        res['total_amount'] = res['untaxed_amount'] + res['tax_amount']
        if self.currency:
            res['total_amount'] = self.currency.round(res['total_amount'])
        return res

    def _compute_taxes(self):
        Tax = Pool().get('account.tax')

        context = self.get_tax_context()

        res = {}
        for line in self.lines:
            # Don't round on each line to handle rounding error
            if line.type != 'line':
                continue
            with Transaction().set_context(**context):
                if(line.product and line.product.dont_multiply):
                    taxes = Tax.compute(line.taxes, line.unit_price,
                        1.0)
                else:
                    taxes = Tax.compute(line.taxes, line.unit_price,
                        line.quantity)
            for tax in taxes:
                key, val = self._compute_tax(tax, self.type)
                val['invoice'] = self.id
                if not key in res:
                    res[key] = val
                else:
                    res[key]['base'] += val['base']
                    res[key]['amount'] += val['amount']
        for key in res:
            for field in ('base', 'amount'):
                res[key][field] = self.currency.round(res[key][field])
        return res

class InvoiceLine(ModelSQL, ModelView):
    'Invoice Line'
    __name__ = 'account.invoice.line'

    def on_change_with_amount(self):
        if self.type == 'line':
            currency = (self.invoice.currency if self.invoice
                else self.currency)
            if (self.product and self.product.dont_multiply):
                amount = self.unit_price or Decimal('0.0')
            else:
                amount = (Decimal(str(self.quantity or '0.0'))
                  * (self.unit_price or Decimal('0.0')))
            if currency:
                return currency.round(amount)
            return amount
        return Decimal('0.0')

    def _compute_taxes(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        Currency = pool.get('currency.currency')

        context = self.invoice.get_tax_context()
        res = []
        if self.type != 'line':
            return res
        with Transaction().set_context(**context):
            if (self.product and self.product.dont_multiply):
                taxes = Tax.compute(self.taxes, self.unit_price, 1.0)
            else:
                taxes = Tax.compute(self.taxes, self.unit_price, self.quantity)
        for tax in taxes:
            if self.invoice.type in ('out_invoice', 'in_invoice'):
                base_code_id = (tax['tax'].invoice_base_code.id
                    if tax['tax'].invoice_base_code else None)
                amount = tax['base'] * tax['tax'].invoice_base_sign
            else:
                base_code_id = (tax['tax'].credit_note_base_code.id
                    if tax['tax'].credit_note_base_code else None)
                amount = tax['base'] * tax['tax'].credit_note_base_sign
            if base_code_id:
                with Transaction().set_context(
                        date=self.invoice.currency_date):
                    amount = Currency.compute(self.invoice.currency,
                        amount, self.invoice.company.currency)
                res.append({
                        'code': base_code_id,
                        'amount': amount,
                        'tax': tax['tax'].id if tax['tax'] else None,
                        })
        return res

    def get_invoice_taxes(self, name):
        pool = Pool()
        Tax = pool.get('account.tax')
        Invoice = pool.get('account.invoice')

        if not self.invoice:
            return
        context = self.invoice.get_tax_context()
        taxes_keys = []
        with Transaction().set_context(**context):
            if (self.product and self.product.dont_multiply):
                taxes = Tax.compute(self.taxes, self.unit_price, 1.0)
            else:
                taxes = Tax.compute(self.taxes, self.unit_price, self.quantity)
        for tax in taxes:
            key, _ = Invoice._compute_tax(tax, self.invoice.type)
            taxes_keys.append(key)
        taxes = []
        for tax in self.invoice.taxes:
            if tax.manual:
                continue
            base_code_id = tax.base_code.id if tax.base_code else None
            tax_code_id = tax.tax_code.id if tax.tax_code else None
            tax_id = tax.tax.id if tax.tax else None
            key = (base_code_id, tax.base_sign,
                tax_code_id, tax.tax_sign,
                tax.account.id, tax_id)
            if key in taxes_keys:
                taxes.append(tax.id)
        return taxes

