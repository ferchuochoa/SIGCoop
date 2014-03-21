from proteus import config, Model
from decimal import Decimal

c = config.set_trytond(database_name="probar_multi2", database_type="postgresql", password="admin", config_file="/home/tryton/runtime/trytond.conf")

def create_prod(tax):
  prod_templ = Model.get('product.template')
  uom = Model.get('product.uom')
  pt1_uom = uom.find([('name', '=', 'Unidad')])[0]
  account = Model.get('account.account')
  pt1_acc_revenue = account.find([('name', '=', 'Ingresos principal')])[0]
  pt1 = prod_templ()
  pt1.name = "Escarapela"
  pt1.active = True
  pt1.salable = True
  pt1.type = "goods"
  pt1.taxes_category = False
  pt1.account_category = False
  pt1.sale_uom = pt1_uom
  pt1.default_uom = pt1_uom
  pt1.dont_multiply = True
  #properties
  pt1.list_price = Decimal(32.00)
  pt1.cost_price = Decimal(44.00)
  pt1.cost_price_method = "fixed"
  pt1.account_revenue = pt1_acc_revenue 
  pt1.customer_taxes.append(tax)
  pt1.save()
  return pt1

def create_tax():
  tax = Model.get('account.tax')
  account = Model.get('account.account')

  t1_inv_acc = account.find([('name', '=', 'Efectivo principal')])[0]
  t1 = tax()
  t1.type = "percentage"
  t1.invoice_account = t1_inv_acc
  t1.credit_note_account = t1_inv_acc
  t1.rate = Decimal('0.29')
  t1.description = "nuevoooo Creado desde proteus descripcion"
  t1.name =  "nuevoooo Creado desde proteus name"
  t1.save()
  return t1

if __name__ == "__main__":
  print create_prod(create_tax())

