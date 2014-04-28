from trytond.pool import Pool
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from decimal import Decimal
from trytond.transaction import Transaction
import logging
logger = logging.getLogger('sale')

class CrearVentasStart(ModelView):
    'Crear Ventas Start'
    __name__ = 'wizard_ventas.crear_ventas.start'
    periodo = fields.Char('Periodo')#, required=True)
    categoria = fields.Many2One('product.price_list', 'Categoria')#, required=True)
    fecha_vencimiento_1 = fields.Date('1er Fecha de Vencimiento')#, required=True)
    fecha_vencimiento_2 = fields.Date('2da Fecha de Vencimiento')#, required=True)
    ruta = fields.Integer('Ruta')#, required=True)

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

    def buscar(self, modelo, atributo, abuscar):
        search = modelo.search([atributo, '=', abuscar])
        if search:
            return search[0]
        else:
            return None

    def buscar_cliente(self, id_suministro):
        Suministro = Pool().get('sigcoop_usuario.suministro')
        suministro = self.buscar(Suministro, "id", id_suministro)
        if suministro is not None:
            return suministro.usuario_id
        else:
            return None

    def construir_descripcion(self):
        return "Descripcion"

    def crear_sale_line(self, amount, product, customer, price_list):
        SaleLine = Pool().get('sale.line')
        #Product = Pool().get('product.product')
        new_line = SaleLine(
                product=product,
                quantity=Decimal(amount),
                description="descripcion",
                unit=product.default_uom,
                )
        with Transaction().set_context({"price_list": price_list, "customer": customer}):
            new_line.unit_price = product.get_sale_price([product], amount)[product.id]
        #new_line.taxes.append()
        return new_line

    def crear_sale_lines(self, concepto, cantidad_consumida, customer, price_list):
        ret = []
        ProductoConsumo = Pool().get('sigcoop_wizard_ventas.producto_consumo')
        producto_consumo_list = ProductoConsumo.search([('concepto', '=', concepto)])
        for producto_consumo in producto_consumo_list:
            cantidad = producto_consumo.cantidad_fija and producto_consumo.cantidad or cantidad_consumida
            ret.append(self.crear_sale_line(cantidad, producto_consumo.producto_id, customer, price_list))
        logger.error("Las sale lines son:")
        logger.error(ret)
        return ret

    def get_extra_taxes(self, product, suministro, party):
        ret = []
        if product.aplica_ap:
            ret.append(suministro.impuesto_alumbrado)
        """
        if product.aplica_iva:
            pedimos el condition_iva a party y determinamos el tipo de impuesto a agregar
            pass
        if product.aplica_iibb:
            preguntamos si el party esta exento
            igual a alumbrado
            pass
        """
        return ret

    def crear_sale(self, suministro, cantidad_consumida, concepto):
        """
        Crea una instancia de sale.sale
        """
        Sale = Pool().get('sale.sale')

        party = suministro.usuario_id
        price_list = suministro.lista_precios
        sale = Sale(
                party=party,
                price_list=price_list,
                description="Sale para %s" % (self.construir_descripcion(),)
        )
        sale.lines = self.crear_sale_lines(concepto, cantidad_consumida, party, price_list)
        sale.save()
        import pudb; pu.db
        Tax = Pool().get('account.tax')
        for i in sale.lines:
            tax_ids = i.on_change_product().get("taxes")#lista de ids
            tax_browse_records = Tax.browse(tax_ids) or []
            extra_tax_browse_records = self.get_extra_taxes(i.product, suministro, party)
            i.taxes = tuple(tax_browse_records) + tuple(extra_tax_browse_records)
            i.save()
        sale.save()

    def transition_crear(self):
        """
        Esta es la primer transicion que se ejecuta cuando ingresamos los datos
        de facturacion.
        """
        Consumos = Pool().get('sigcoop_consumos.consumo')
        filtro_consumo = [
                ('estado', '=', '1'),
                ('periodo', '=', self.start.periodo),
                ('id_suministro.ruta', '=', self.start.ruta),
                ('id_suministro.lista_precios', '=', self.start.categoria),
        ]
        logger.error("===========Iterando sobre los consumos============")
        for consumo in Consumos.search(filtro_consumo):
            logger.error(consumo)
            self.crear_sale(consumo.id_suministro, consumo.consumo_neto, consumo.concepto)
        logger.error("===========/Iterando sobre los consumos============")
        return 'exito'
