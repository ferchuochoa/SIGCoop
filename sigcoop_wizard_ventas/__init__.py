#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .producto_consumo import ProductoConsumo
from .product import Template
from .wizard_ventas import CrearVentasStart, CrearVentas, CrearVentasExito

def register():
    Pool.register(
        ProductoConsumo,
        Template,
        CrearVentasStart,
        CrearVentasExito,
        module='sigcoop_wizard_ventas', type_='model')

    Pool.register(
        CrearVentas,
        module='sigcoop_wizard_ventas', type_='wizard')
