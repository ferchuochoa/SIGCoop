from trytond.pool import Pool
from .party import *
from .familiar import Familiar


def register():
    Pool.register(
        Party,
        Familiar,
        module='sigcoop_usuario', type_='model'
    )
