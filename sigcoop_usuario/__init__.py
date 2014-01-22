from trytond.pool import Pool
from .party import *

def register():
  Pool.register(
     Party,
     module='sigcoop_usuario', type_='model'
  )
