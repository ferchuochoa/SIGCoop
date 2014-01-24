from trytond.pool import Pool
from .party import *
from .rango import Rango

def register():
  Pool.register(
     Party,
     Rango,
     module='sigcoop_usuario', type_='model'
  )
