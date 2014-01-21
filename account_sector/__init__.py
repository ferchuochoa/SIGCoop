from trytond.pool import Pool
from .account import *

def register():
  Pool.register(
     Sector,
     Account,
     module='account_sector', type_='model'
  )
