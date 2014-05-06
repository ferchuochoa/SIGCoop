#-*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, fields

__all__ = ['ProductoConsumo']
CONCEPTOS = [
    ('1', 'Cargo variable'),
    ('2', 'Cargo variable Pico'),
    ('3', 'Cargo variable Fuera de pico'),
    ('4', 'Cargo variable Valle'),
    ('5', 'Cargo variable Resto'),
    ('6', 'Potencia Pico'),
    ('7', 'Potencia Resto'),
    ('8', 'Exceso potencia Pico'),
    ('9', 'Exceso potencia Resto'),
    ('10', 'Cargo perdida Transformador'),
    ('11', 'Recargos x Bajo Cos Fi'),
]

class ProductoConsumo(ModelSQL, ModelView):
    "Producto Consumo"
    __name__ = "sigcoop_wizard_ventas.producto_consumo"

    producto_id = fields.Many2One('product.product', 'Producto')
    tarifa_id = fields.Many2One('product.price_list', 'Tarifa')
    concepto = fields.Selection(CONCEPTOS, 'Concepto')
    cantidad_fija = fields.Boolean('Cantidad fija?')
    cantidad = fields.Integer('Cantidad')
