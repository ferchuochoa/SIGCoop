#This file is part of Tryton.  The COPYRIGHT file at the top level
#of this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import ModelView, ModelSQL, fields

__all__ = ['Template']
__metaclass__ = PoolMeta

class Template(ModelSQL, ModelView):
    "Product Template"
    __name__ = "product.template"

    aplica_iva = fields.Boolean('Aplicar iva')
    aplica_ap = fields.Boolean('Aplicar alumbrado publico')
    aplica_iibb = fields.Boolean('Aplicar ingresos brutos')
