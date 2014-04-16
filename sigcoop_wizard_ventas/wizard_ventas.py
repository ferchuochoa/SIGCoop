from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, StateTransition, Button

CATEGORIAS = [
("T1AP", "T1AP Alumbrado Publico"),
("T1GAC", "T1GAC Servicio General Alto Consumo"),
("T1GBC", "T1GBC Servicio General Bajo Consumo"),
("T1R", "T1R Residencial"),
("T1R2", "T1R Residencial Social"),
("T2BT", "T2BT Baja Tension"),
("T2MT", "T2MT Media Tension"),
("T3BT", "T3BT Baja Tension (>300KW)"),
("T3BT2", "T3BT Baja Tension (50 a 300KW)"),
("T3MT", "T3MT Media Tension (>300KW)"),
("T3MT2", "T3MT Media Tension (50 a 300KW)"),
("T4", "T4 Rural"),
("T5BT", "T5BT Baja Tension (>300KW)"),
("T5BT2", "T5BT Baja Tension (50 a 300KW)"),
("T5MT", "T5MT Media Tension (>300KW)"),
("T5MT2", "T5MT Media Tension (50 a 300KW)"),
]

class CrearVentasStart(ModelView):
    'Crear Ventas Start'
    __name__ = 'wizard_ventas.crear_ventas.start'
    periodo = fields.Integer('Periodo')
    categoria = fields.Selection(CATEGORIAS, 'Categoria')
    fecha_vencimiento_1 = fields.Date('1er Fecha de Vencimiento')
    fecha_vencimiento_2 = fields.Date('2da Fecha de Vencimiento')
    ruta = fields.Integer('Ruta')

class CrearVentasExito(ModelView):
    'Crear Ventas Exito'
    __name__ = 'wizard_ventas.crear_ventas.exito'

class CrearVentas(Wizard):
    'Crear Ventas'
    __name__ = 'wizard_ventas.crear_ventas'

    start = StateView('wizard_ventas.crear_ventas.start',
        'wizard_ventas.crear_ventas_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Crear Ventas', 'crear', 'tryton-ok', default=True),
            ])

    exito = StateView('wizard_ventas.crear_ventas.exito',
        'wizard_ventas.crear_ventas_exito_view_form', [
            Button('Ok', 'end', 'tryton-ok', default=True),
            ])

    crear = StateTransition()

    def transition_crear(self):
        return 'exito'
