from proteus import config, Model
from decimal import Decimal
from datetime import datetime

ahora = datetime.now()

c = config.set_trytond(database_name="probar_multi2", database_type="postgresql", password="admin", config_file="/home/tryton/runtime/trytond.conf")

Product = Model.get('product.product')

prod = {
        "id" : 1,
        "model" : "product.template",
        "uom" : ("product.uom", [("name", "=", "Unidad")]),
        "name" : "%s:%s Nuevo Producto creado desde create_entity" % (str(ahora.hour), str(ahora.minute)),
        "active" : True,
        "salable" : True,
        "type" : "service",
        "taxes_category": False,
        "account_category": False,
        "sale_uom": ("product.uom", [("name", "=", "Unidad")]),
        "default_uom": ("product.uom", [("name", "=", "Unidad")]),
        "dont_multiply": False,
        "list_price" : Decimal(32.00),
        "cost_price" : Decimal(44.00),
        "cost_price_method" : "fixed",
        "account_revenue" : ("account.account", [('name', '=', 'Ingresos principal')]),
        "customer_taxes" : ["account.tax", [('name', '=', 'Porcentaje 10p')]]
}

def create_entity(values):
    if not values.get("model"):
        print "Falta el modelo. Que estamos haciendo??"
        return None
    if not (values.get("id")):
        print "Falta el id. Que estamos haciendo??"
        return None
    model = values.pop("model")
    _id = values.pop("id")

    print "Creando la entidad %s para el registro numero %s" % (model, _id)

    #Contructor del modelo
    const = Model.get(model)
    entity = const()
    #import pdb;pdb.set_trace()

    save_for_last = []

    for k,v in values.iteritems():
        if (isinstance(v, tuple)):
            ref = Model.get(v[0]).find(v[1])[0]
            setattr(entity, k, ref)
        elif (isinstance(v, list)):
            constructor = Model.get(v[0])
            to_save = []
            for elem in v[1]:
                #getattr(entity, k).append(constructor.find([elem])[0])
                to_save.append(constructor.find([elem])[0])
                #entity.save()
            save_for_last.append((k, to_save))
        else:
            setattr(entity, k, v)
    #print "Antes de guardar"
    for i in save_for_last:
        print i[0]
        print i[1]
        getattr(entity, i[0]).extend(i[1])
    print entity.customer_taxes
    entity.save()
    return entity

def create_prod(tax):
    prod_templ = Model.get('product.template')
    uom = Model.get('product.uom')
    pt1_uom = uom.find([('name', '=', 'Unidad')])[0]
    account = Model.get('account.account')
    pt1_acc_revenue = account.find([('name', '=', 'Ingresos principal')])[0]
    pt1 = prod_templ()
    pt1.name = str(datetime.today())
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
    t1.name =  "Creado desde proteus name"
    t1.save()
    return t1

def create_pricelist_line(price_list):
    pl_line = Model.get('product.price_list.line')
    pl_l1 = pl_line()
    pl_l1.price_list = price_list
    pl_l1.product = Product.find([('name', '=', 'Termito')])[0]
    #sequence
    pl_l1.quantity = 23
    pl_l1.unit_digits = 12
    pl_l1.formula = "unit_price * 2"
    pl_l1.save()
    return pl_l1

def create_pricelist():
    price_list = Model.get('product.price_list')
    pl = price_list()
    pl.name = "mi pricelist"
    pl.company = Model.get('company.company').find([])[0]
    pl.save()
    return pl

if __name__ == "__main__":
    #print create_prod(create_tax())
    #print create_pricelist_line(create_pricelist())
    print create_entity(prod)
