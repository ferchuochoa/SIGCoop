from trytond.pool import Pool
from .account import *

def register():
  Pool.register(
     SectorTemplate,
     Sector,
     AccountTemplate,
     Account,
     CreateChartAccount,
     module='account_sector', type_='model'
  )
  Pool.register(
     CreateChart,
     module='account_sector', type_='wizard'
  )
