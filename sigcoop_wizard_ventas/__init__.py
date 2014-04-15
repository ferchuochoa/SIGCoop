#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .producto_consumo import ProductoConsumo
from .product import Template

def register():
    Pool.register(
        ProductoConsumo,
        Template,
        module='sigcoop_wizard_ventas', type_='model')
