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
    print "=============================="
    print row
    print "=============================="
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

def translate_to_product(_id, row):
    ret = dict()
    ret["model"] = "product.template"
    ret["id"] = _id

    ret["name"] = row["Nombre"]
    ret["salable"] = row["Vendible"] == "True"
    ret["type"] = row["Tipo"]
    ret["dont_multiply"] = row[""]
    ret["list_price"] = row["Precio de lista"]
    ret["cost_price"] = row["Precio de costo"]

    ret["default_uom"] = ("product.uom", [("name", "=", row["Udm por defecto"])])
    ret["account_revenue"] = ("account.account", [('code', '=', row["Cuenta de ingresos"])])
    ret["customer_taxes"] = ["account.tax", [('name', '=', '%s' %i ) for i in row["Impuestos de cliente"].split("#")]]

    return ret

def create_entities(csv_reader, translator):
    for _id, row in enumerate(csv_reader):
        #Traducimos cada fila al diccionario que corresponde y usamos este diccionario
        #para crear la entidad
        create_entity(translator(_id, row))
        #print translator(_id, row)

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
    save_for_last = []

    for k,v in values.iteritems():
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
        create_entities(csv.DictReader(fi, delimiter=";"), translate_to_tax)

if __name__ == "__main__":
    main()
