from trytond.pool import Pool
from .medidor import *

def register():
    Pool.register(
        Medidor,
        module='sigcoop_medidor', type_='model')