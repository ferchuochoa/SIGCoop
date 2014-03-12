#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pyson import Eval, Not, Equal, Or, Bool
from trytond.transaction import Transaction
from decimal import Decimal
from trytond.pool import Pool, PoolMeta

import logging

__all__ = ['SaleLine', 'Sale']
__metaclass__ = PoolMeta
_ZERO = Decimal(0)


class Sale(Workflow, ModelSQL, ModelView):
  'Sale'
  __name__ = 'sale.sale'

  def on_change_lines(self):
    logging.getLogger('sale').warning("En onchange lines!!!!!!!!!!!!!!!!11")
    pool = Pool()
    Tax = pool.get('account.tax')
    Invoice = pool.get('account.invoice')

    res = {
        'untaxed_amount': Decimal('0.0'),
        'tax_amount': Decimal('0.0'),
        'total_amount': Decimal('0.0'),
        }

    if self.lines:
      taxes = {}
      for line in self.lines:
        if getattr(line, 'type', 'line') != 'line':
            continue
        res['untaxed_amount'] += line.amount or Decimal(0)
        tax_list = ()
        with Transaction().set_context(self.get_tax_context()):
          if (line.dont_multiply):
            tax_list = Tax.compute(getattr(line, 'taxes', []), line.unit_price or Decimal('0.0'), 1.0)
          else:
            tax_list = Tax.compute(getattr(line, 'taxes', []), line.unit_price or Decimal('0.0'), line.quantity or 0.0)
        for tax in tax_list:
          key, val = Invoice._compute_tax(tax, 'out_invoice')
          if not key in taxes:
            taxes[key] = val['amount']
          else:
            taxes[key] += val['amount']
      if self.currency:
        for key in taxes:
          res['tax_amount'] += self.currency.round(taxes[key])
    if self.currency:
      res['untaxed_amount'] = self.currency.round(res['untaxed_amount'])
      res['tax_amount'] = self.currency.round(res['tax_amount'])
    res['total_amount'] = res['untaxed_amount'] + res['tax_amount']
    if self.currency:
      res['total_amount'] = self.currency.round(res['total_amount'])
    return res

  def get_tax_amount(self):
    pool = Pool()
    Tax = pool.get('account.tax')
    Invoice = pool.get('account.invoice')

    context = self.get_tax_context()
    taxes = {}
    for line in self.lines:
      if line.type != 'line':
        continue
      with Transaction().set_context(context):
        if (line.dont_multiply):
          tax_list = Tax.compute(line.taxes, line.unit_price,
              1.0)
        else:
          tax_list = Tax.compute(line.taxes, line.unit_price,
              line.quantity)
      # Don't round on each line to handle rounding error
      for tax in tax_list:
        key, val = Invoice._compute_tax(tax, 'out_invoice')
        if not key in taxes:
          taxes[key] = val['amount']
        else:
          taxes[key] += val['amount']
    return sum((self.currency.round(tax) for tax in taxes.values()), _ZERO)

class SaleLine(ModelSQL, ModelView):
  __name__ = 'sale.line'
  dont_multiply = fields.Boolean("No multiplicar por cantidad")#, on_change=['product', 'dont_multiply'])
  amount = fields.Function(fields.Numeric('Amount',
          digits=(16, Eval('_parent_sale', {}).get('currency_digits', 2)),
          states={
              'invisible': ~Eval('type').in_(['line', 'subtotal']),
              'readonly': ~Eval('_parent_sale'),
              }, on_change_with=['type', 'quantity', 'unit_price', 'unit',
              '_parent_sale.currency', 'dont_multiply'],
          depends=['type', 'dont_multiply']), 'get_amount')

  """
  def on_change_amount(self):
    logging.getLogger('sale').warning("************************")
    logging.getLogger('sale').warning("OTRO ON_CHANGE_AMOUNT%s" % self.dont_multiply)
    logging.getLogger('sale').warning("************************")
    return {'amount': Decimal(43.0)}

  def on_change_dont_multiply(self):
    return {'amount': Decimal(34.0)}
  """

  def on_change_with_amount(self):
    #import pdb;pdb.set_trace()
    logging.getLogger('sale').warning("USANDO GET: %s " % self._values.get('dont_multiply'))
    if self._values.get('dont_multiply') and self.type == 'line':
      logging.getLogger('sale').warning("EN on_change_with_amount tenemos el valor de dont")
      return (self.unit_price or Decimal('0.0'))
    else:
      ret = super(SaleLine, self).on_change_with_amount()
      logging.getLogger('sale').warning("EN on_change_with_amount no tenemos el valor de dont retornamos: %s" % ret)
      return ret

  def get_amount(self, name):
    #import pdb;pdb.set_trace()
    if self.type == 'line' and self.dont_multiply:
      logging.getLogger('sale').warning("AHORA dentro de GET_AMOUNT retornamos el dont")
      return self.unit_price
    else:
      logging.getLogger('sale').warning("AHORA dentro de GET_AMOUNT retornamos el ret")
      return super(SaleLine, self).get_amount(name) 
    """
    logging.getLogger('sale').warning("====================================")
    logging.getLogger('sale').warning("AHORA dentro de GET_AMOUNT %s" % self.dont_multiply)
    logging.getLogger('sale').warning("====================================")
        if self.type == 'line':
            return self.sale.currency.round(
                Decimal(str(self.quantity)) * self.unit_price)
        elif self.type == 'subtotal':
            amount = Decimal('0.0')
            for line2 in self.sale.lines:
                if line2.type == 'line':
                    amount += line2.sale.currency.round(
                        Decimal(str(line2.quantity)) * line2.unit_price)
                elif line2.type == 'subtotal':
                    if self == line2:
                        break
                    amount = Decimal('0.0')
            return amount
        return Decimal('0.0')
    logging.getLogger('sale').warning("GET_AMOUNT %s" % ret)
    logging.getLogger('sale').warning("GET_AMOUNT %s" % self.dont_multiply)
    logging.getLogger('sale').warning("GET_AMOUNT %s" % type(self))
    return ret
    """
