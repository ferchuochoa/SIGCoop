from trytond.pool import Pool
from .medidor import *
from .suministro import *

def register():
    Pool.register(
        Medidor,
        Suministro,
        SuministroMedidor,
        module='sigcoop_medidor', type_='model')