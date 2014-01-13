from trytond.pool import Pool
from .account import *

def register():
  Pool.register(
     Account,
     Sector,
     module='account_sector', type_='model'
  )
