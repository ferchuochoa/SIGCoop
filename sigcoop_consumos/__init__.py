from trytond.pool import Pool
from .consumo import *
from .suministro import *

def register():
  Pool.register(
     Consumo,
     Suministro,
     module='sigcoop_consumos', type_='model'
  )
