from trytond.pool import Pool
from .party import *
from .familiar import Familiar
from .suministro import Suministro
from .aporte import Aporte
from .rango import Rango

def register():
    Pool.register(
        Party,
        Suministro,
        Familiar,
        Aporte,
	Rango,
        module='sigcoop_usuario', type_='model'
    )

