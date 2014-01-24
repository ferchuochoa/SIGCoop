from trytond.pool import Pool
from .party import *
from .familiar import Familiar
from .suministro import Suministro


def register():
    Pool.register(
        Party,
        Suministro,
        Familiar,
        module='sigcoop_usuario', type_='model'
    )
