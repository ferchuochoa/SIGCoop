#This file is part of Tryton.  The COPYRIGHT file at the top level
#of this repository contains the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.model import Workflow, ModelView, ModelSQL, fields

__all__ = ['Template']
__metaclass__ = PoolMeta

class Template(ModelSQL, ModelView):
    "Product Template"
    __name__ = "product.template"

    dont_multiply = fields.Boolean('Producto de precio independiente de la cantidad')
