from trytond.pool import Pool
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from decimal import Decimal
from trytond.transaction import Transaction
import logging
import itertools
logger = logging.getLogger('sale')
REQUERIDO = False

class CrearVentasStart(ModelView):
    'Crear Ventas Start'
    __name__ = 'wizard_ventas.crear_ventas.start'
    periodo = fields.Char('Periodo', required=REQUERIDO)
    categoria = fields.Many2One('product.price_list', 'Categoria', required=REQUERIDO)
    fecha_vencimiento_1 = fields.Date('1er Fecha de Vencimiento', required=REQUERIDO)
    fecha_vencimiento_2 = fields.Date('2da Fecha de Vencimiento', required=REQUERIDO)
    ruta = fields.Integer('Ruta', required=REQUERIDO)

    @classmethod
    def default_periodo(cls):
        return '1'

    @classmethod
    def default_ruta(cls):
        return 1

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

    def buscar(self, modelo, atributo, valor):
        search = modelo.search([atributo, '=', valor])
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
        """
        Creamos una linea de ventas de acuerdo a los parametros que recibimos.
        """
        SaleLine = Pool().get('sale.line')
        new_line = SaleLine(
                product=product,
                quantity=Decimal(amount),
                description="descripcion",
                unit=product.default_uom,
                )
        with Transaction().set_context({"price_list": price_list, "customer": customer}):
            new_line.unit_price = product.get_sale_price([product], amount)[product.id]
        return new_line

    def crear_sale_lines_dependientes_consumo(self, concepto, cantidad_consumida, customer, price_list):
        """
        Creamos las lineas de venta que dependen de la cantidad de kw consumidos.
        """
        ret = []
        ProductoConsumo = Pool().get('sigcoop_wizard_ventas.producto_consumo')
        producto_consumo_list = ProductoConsumo.search([('concepto', '=', concepto), ('tarifa_id', '=', price_list)])
        for producto_consumo in producto_consumo_list:
            cantidad = producto_consumo.cantidad_fija and producto_consumo.cantidad or cantidad_consumida
            ret.append(self.crear_sale_line(cantidad, producto_consumo.producto_id, customer, price_list))
        return ret

    def crear_sale_lines_independientes_consumo(self, concepto, cantidad_consumida, party, price_list):
        ret = []
        #TODO: tal vez es mas eficiente hacer un search sobre PriceList
        filtro_producto = lambda x: (x.product.tipo_cargo == 'fijo' and x.product.tipo_producto == 'cargos')
        productos = map(lambda x: x.product, filter(filtro_producto, price_list.lines))
        for producto in productos:
            ret.append(self.crear_sale_line(1, producto, party, price_list))
        return ret

    def crear_sale_lines_sin_impuestos(self, concepto, cantidad_consumida, party, price_list):
        ret = []
        #TODO: tal vez es mas eficiente hacer un search sobre PriceList
        filtro_producto = lambda x: (x.product.tipo_cargo == 'fijo' and x.product.tipo_producto == 'varios')
        productos = map(lambda x: x.product, filter(filtro_producto, price_list.lines))
        for producto in productos:
            ret.append(self.crear_sale_line(1, producto, party, price_list))
        return ret

    def get_extra_taxes(self, product, suministro, party):
        """
        Retornamos una lista de account.tax con los impuestos que tenemos que calcular
        dinamicamente.
        """
        ret = []
        if product.aplica_ap and suministro.impuesto_alumbrado:
            ret.append(suministro.impuesto_alumbrado)
        """
        if product.aplica_iva:
            pedimos el condition_iva a party y determinamos el tipo de impuesto a agregar
            chequear que el impuesto este seteado
            pass
        if product.aplica_iibb:
            preguntamos si el party esta exento
            igual a alumbrado
            chequear que el impuesto este seteado
            pass
        """
        return ret

    def crear_sale(self, lista_consumos):
        """
        lista_consumos[0]: id del suministro
        lista_consumos[1]: iterador sobre Consumo para el suministro
        """
        #Creamos la venta a la que le vamos a asociar las lineas de venta
        Sale = Pool().get('sale.sale')
        Suministro = Pool().get('sigcoop_usuario.suministro')
        suministro = Suministro.browse([lista_consumos[0]])[0]
        party = suministro.usuario_id
        price_list = suministro.lista_precios
        sale = Sale(
                party=party,
                price_list=price_list,
                description="Sale para %s" % (self.construir_descripcion(),)
        )

        #Creamos las lineas para los distintos tipos de productos
        sale_lines = []
        for i in lista_consumos[1]:
            sale_lines.extend(
                    self.crear_sale_lines_dependientes_consumo(
                        i.concepto, i.consumo_neto, party, price_list
                    ))
            sale_lines.extend(
                    self.crear_sale_lines_independientes_consumo(
                        i.concepto, i.consumo_neto, party, price_list
                    ))
            sale_lines.extend(
                    self.crear_sale_lines_sin_impuestos(
                        i.concepto, i.consumo_neto, party, price_list
                    ))
        sale.lines = sale_lines
        sale.save()

        #Aplicamos los impuestos que correspondan a cada linea de venta
        Tax = Pool().get('account.tax')
        for i in sale.lines:
            tax_ids = i.on_change_product().get("taxes")#lista de ids
            tax_browse_records = Tax.browse(tax_ids) or []
            logger.error("-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=")
            for t in tax_browse_records:
                logger.error(t.description)
            logger.error("-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=")
            extra_tax_browse_records = self.get_extra_taxes(i.product, suministro, party)
            i.taxes = tuple(tax_browse_records) + tuple(extra_tax_browse_records)
            i.save()
        sale.save()

    def agrupar_por_suministro(self, lista_consumos):
        """
        Retornamos los consumos agrupados por suministro:
            [
            (id suministro 1, [consumo 1, consumo 2, ...]),
            (id suministro 2, [consumo 3, consumo 4, ...])
            ]
        """
        return itertools.groupby(lista_consumos, lambda x: x.id_suministro.id)

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
        map(self.crear_sale, self.agrupar_por_suministro(Consumos.search(filtro_consumo)))
        return 'exito'
