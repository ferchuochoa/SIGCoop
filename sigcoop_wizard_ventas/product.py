#This file is part of Tryton.  The COPYRIGHT file at the top level
#of this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import ModelView, ModelSQL, fields

__all__ = ['Template']
__metaclass__ = PoolMeta

TIPO_CARGO = [('fijo', 'Fijo'), ('variable', 'Variable')]
TIPO_PRODUCTO = [('otros', 'Otros'), ('cargos', 'Cargos'), ('varios', 'Varios')]

class Template(ModelSQL, ModelView):
    "Product Template"
    __name__ = "product.template"

    aplica_iva = fields.Boolean('Aplicar iva')
    aplica_ap = fields.Boolean('Aplicar alumbrado publico')
    aplica_iibb = fields.Boolean('Aplicar ingresos brutos')
    tipo_cargo = fields.Selection(TIPO_CARGO, 'Tipo cargo')
    tipo_producto = fields.Selection(TIPO_PRODUCTO, 'Tipo Producto')
