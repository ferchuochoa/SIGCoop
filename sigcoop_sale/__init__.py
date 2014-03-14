#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .sale import *
from .product import *
from .invoice import *

def register():
    Pool.register(
        SaleLine,
        Template,
        Sale,
        Invoice,
        InvoiceLine,
        module='sigcoop_sale', type_='model')
