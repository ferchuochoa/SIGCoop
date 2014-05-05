from trytond.pool import Pool
from .consumo import *
from .suministro import *
from .medidor import *

def register():
    Pool.register(
        Consumo,
        Suministro,
        Medidor,    
        ImportacionStart,
        ImportacionResumen,
        module='sigcoop_consumos', type_='model')

    Pool.register(
        ImportacionConsumos,
        module='sigcoop_consumos', type_='wizard')
