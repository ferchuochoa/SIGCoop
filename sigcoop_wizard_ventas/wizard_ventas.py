from trytond.pool import Pool
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
import logging
from decimal import Decimal
from trytond.transaction import Transaction

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
        'sigcoop_wizard_ventas.crear_ventas_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Crear Ventas', 'crear', 'tryton-ok', default=True),
            ])

    exito = StateView('wizard_ventas.crear_ventas.exito',
        'sigcoop_wizard_ventas.crear_ventas_exito_view_form', [
            Button('Ok', 'end', 'tryton-ok', default=True),
            ])

    crear = StateTransition()

    def crear_sale_lines(sale, price_list, customer):
        """
        Para las sale_lines, necesitamos:
            quantity
            product
        """
        ret = []
        SaleLine = Pool().get('sale.line')
        Product = Pool().get('product.product')
        cargo_variable = Product.search([('name', '=', 'Cargo Variable T1R')])[0]
        new_line = SaleLine(
                product=cargo_variable,
                quantity=Decimal(120.0),
                description="descripcion",
                unit=cargo_variable.default_uom,
                )
        with Transaction().set_context({"price_list": price_list, "customer": customer}):
            new_line.unit_price = cargo_variable.get_sale_price([cargo_variable], 120.0)[cargo_variable.id]
            ret.append(new_line)
        return ret

    def transition_crear(self):
        """
        Creamos las ventas a partir de los consumos que correspondan.
        Ver sale.py linea 721 para creacion invoice
        Necesitamos:
            party : party.party
            price_list : m2o product.price_list
            lines : o2m sale.line
        """
        Sale = Pool().get('sale.sale')
        Party = Pool().get('party.party')
        PriceList = Pool().get('product.price_list')
        sale = Sale(
                party=Party.search([])[0],
                price_list=PriceList.search([])[0],
                description="Creado desde el wizard 2"
        )
        sale.lines = self.crear_sale_lines(PriceList.search([])[0], Party.search([])[0])
        sale.save()
        return 'exito'
