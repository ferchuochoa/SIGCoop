"""
from trytond.pool import Pool
from .tasa import Tasa

def register():
    Pool.register(
        Tasa,
        module='sigcoop_tasas', type_='model'
    )
"""
