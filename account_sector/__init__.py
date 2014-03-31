from trytond.pool import Pool
from .account import *

def register():
  Pool.register(
     SectorTemplate,
     Sector,
     AccountTemplate,
     Account,
     module='account_sector', type_='model'
  )
