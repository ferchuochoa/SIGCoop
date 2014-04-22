#-*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, fields

__all__ = ['ProductoConsumo']
CODIGOS = [
    ('1', 'Cargo variable'),
    ('2', 'Cargo variable Pico'),
    ('3', 'Cargo variable Valle'),
    ('4', 'Cargo variable Resto'),
    ('5', 'Potencia Pico'),
    ('6', 'Potencia Resto'),
    ('7', 'Exceso potencia Pico'),
    ('8', 'Exceso potencia Resto'),
    ('9', 'Cargo perdida Transformador'),
    ('10', 'Recargos x Bajo Cos Fi'),
]

class ProductoConsumo(ModelSQL, ModelView):
    "Producto Consumo"
    __name__ = "sigcoop_wizard_ventas.producto_consumo"

    producto_id = fields.Many2One('product.product', 'Producto')
    codigo_consumo = fields.Selection(CODIGOS, 'Codigo consumo')
    cantidad_fija = fields.Boolean('Cantidad fija?')
    cantidad = fields.Integer('Cantidad')
