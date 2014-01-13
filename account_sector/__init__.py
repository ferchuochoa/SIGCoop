from trytond.pool import Pool
from .account import *
from .account_sector import *

def register():
  Pool.register(
     Account,
     Sector,
     module='account_sector', type_='model'
  )
