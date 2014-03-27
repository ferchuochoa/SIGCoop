#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import csv
from proteus import config, Model
from decimal import Decimal
c = config.set_trytond(database_name="probar_multi2", database_type="postgresql", password="admin", config_file="/home/tryton/runtime/trytond.conf")


"""
Nombre
Descripción
Tipo


Cuenta de la factura/Código
Cuenta de la nota de crédito/Código

Importe
Tasa de cambio

No usados:

Cuenta de la factura/Nombre
Cuenta de la nota de crédito/Nombre
Cuenta de la factura/Código
Cuenta de la factura/Nombre
Secuencia
Dígitos de moneda
"""

def translate_to_tax(_id, row):
    ret = {
    "id" : _id,
    "model" : "account.tax",
    "name": row["Nombre"],
    "description": row["Descripción"],
    "type" : row["Tipo"],
    "invoice_account" : ("account.account", [('code', '=', row["Cuenta de la factura/Código"])]),
    "credit_note_account" : ("account.account", [('code', '=', row["Cuenta de la nota de crédito/Código"])]),
    }

    if (ret["type"] == "fixed"):
        ret["amount"] = Decimal(row["Importe"])
    else:
        ret["rate"] = Decimal(row["Tasa de cambio"])

    return ret

"""
Nombre
Vendible
Tipo
Producto de precio independiente de la cantidad
Precio de lista
Precio de costo
UdM por defecto/Nombre
Cuenta de ingresos/Código
Impuestos de cliente/Nombre
Categoria/Nombre

Comprable false por defecto
Consumible false por defecto
"""

def check_category(cat_name):
    cats = Model.get('product.category').find([("name", "=", cat_name)])
    if not cats:
        cat = Model.get('product.category')()
        cat.name = cat_name
        cat.save()
        return cat
    else:
        return cats[0]

def check_uom(uom_name):
    uom = Model.get('product.uom').find([("name", "=", uom_name)])
    if not uom:
        nuom = {
                "id":1,
                "model":"product.uom",
                "name": uom_name,
                "symbol": "Kw",
                "category": ("product.uom.category", [("name","=","Unidades")]),
        }
        return create_entity(nuom)
    else:
        return uom[0]

def translate_to_product(_id, row):
    ret = dict()
    ret["model"] = "product.template"
    ret["id"] = _id

    ret["name"] = row["Nombre"]
    ret["salable"] = row["Vendible"] == "True"
    ret["type"] = row["Tipo"]
    ret["dont_multiply"] = row["Producto de precio independiente de la cantidad"] == "True"
    ret["list_price"] = Decimal(row["Precio de lista"])
    ret["cost_price"] = Decimal(row["Precio de costo"])

    check_category(row["Categoria/Nombre"])
    ret["category"] = ("product.category", [("name", "=", row["Categoria/Nombre"])])

    check_uom(row["UdM por defecto/Nombre"])
    ret["default_uom"] = ("product.uom", [("name", "=", row["UdM por defecto/Nombre"])])

    ret["account_revenue"] = ("account.account", [('code', '=', row["Cuenta de ingresos/Código"])])
    ret["customer_taxes"] = ["account.tax", [('name', '=', '%s' % i ) for i in row["Impuestos de cliente/Nombre"].split("#") if i]]

    return ret

def create_entities(csv_reader, translator, simulate=False):
    for _id, row in enumerate(csv_reader):
        #Traducimos cada fila al diccionario que corresponde y usamos este diccionario
        #para crear la entidad
        if not simulate:
            create_entity(translator(_id, row))
        else:
            print translator(_id, row)

def create_entity(values):
    if not values.get("model"):
        print "Falta el modelo. Que estamos haciendo??"
        return None
    if (values.get("id") is None):
        print "Falta el id. Que estamos haciendo??"
        return None
    model = values.pop("model")
    _id = values.pop("id")

    print "Creando la entidad %s para el registro numero %s" % (model, _id)

    #Contructor del modelo
    const = Model.get(model)
    entity = const()
    save_for_last = []

    for k,v in values.iteritems():
        print "seteando %s con %s" % (str(k), str(v))
        #print "seteando %k con %v" % (str(k), str(v))
        if (isinstance(v, tuple)):
            ref = Model.get(v[0]).find(v[1])[0]
            setattr(entity, k, ref)
        elif (isinstance(v, list)):
            constructor = Model.get(v[0])
            to_save = []
            for elem in v[1]:
                to_save.append(constructor.find([elem])[0])
            save_for_last.append((k, to_save))
        else:
            setattr(entity, k, v)
    for i in save_for_last:
        getattr(entity, i[0]).extend(i[1])
    entity.save()
    return entity


def main():
    fname = sys.argv[1]
    print "Cargando"
    print fname
    #create_entities(csv.DictReader(fname, delimiter=";"), translate_to_product)
    with open(fname) as fi:
        #create_entities(csv.DictReader(fi, delimiter=";"), translate_to_tax)
        create_entities(csv.DictReader(fi, delimiter=";"), translate_to_product, False)

if __name__ == "__main__":
    main()
