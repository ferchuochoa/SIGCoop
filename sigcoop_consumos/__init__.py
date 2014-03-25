from trytond.pool import Pool
from .consumo import *
from .suministro import *

def register():
    Pool.register(
        Consumo,
        Suministro,
        ImportacionStart,
        module='sigcoop_consumos', type_='model')

    Pool.register(
        ImportacionConsumos,
        module='sigcoop_consumos', type_='wizard')
