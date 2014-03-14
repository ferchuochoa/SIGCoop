#-*- coding: utf-8 -*-
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, And, Bool, Equal, Not

__all__ = ['Party']


class Party(ModelSQL, ModelView):
    "Party"
    __name__ = 'party.party'
    #El field asociado nos da a elegir si es asociado o cliente.
    #Por defecto, es cliente ya que el campo es false.
    asociado = fields.Boolean('Es Asociado')
    dir_entrega_factura = fields.Many2One('party.address', 'Direccion entrega factura')
    ruta = fields.Integer('Ruta')
    tipo_identificacion = fields.Selection(
        [
            ('CUIT', 'CUIT'),
            ('CUIL', 'CUIL'),
            ('DNI', 'DNI'),
        ],
        'Tipo de identificacion'
    )
    #Este es el valor de cuil, cuit o dni,
    #segun se seleccione en el selection.
    valor_identificacion = fields.Integer('Valor identificacion')
    #El numero indica el numero de cliente o
    #asociado segun se indique en el campo asociado.
    numero = fields.Integer('Numero de Cliente/Asociado')
    numero_titulo = fields.Integer('Numero de titulo')
    fecha_ingreso = fields.Date('Fecha de ingreso')
    #Referencias muchos a uno
    suministros = fields.One2Many('sigcoop_usuario.suministro', 'usuario_id', 'Suministros')
    rangos = fields.One2Many('sigcoop_usuario.rango', 'asociado', 'Rangos')
    familiares = fields.One2Many('sigcoop_usuario.familiar', 'usuario_id', 'Familiares')
    aportes = fields.One2Many('sigcoop_usuario.aporte', 'usuario_id', 'Familiares')
    iva_condition = fields.Selection(
            [
                ('', ''),
                ('responsable_inscripto', 'Responsable Inscripto'),
                ('exento', 'Exento'),
                ('consumidor_final', 'Consumidor Final'),
                ('monotributo', 'Monotributo'),
                ('no_alcanzado', 'No alcanzado'),
            ],
            'Condicion ante el IVA',
            states={
                'readonly': ~Eval('active', True),
                #'required': Equal(Eval('vat_country'), 'AR'), En account_invoice_ar, definen vat country
                },
            depends=['active'],
            )
    iibb_type = fields.Selection(
            [
                ('', ''),
                ('cm', 'Convenio Multilateral'),
                ('rs', 'Regimen Simplificado'),
                ('exento', 'Exento'),
            ],
            'Tipo de Inscripcion de II BB',
            states={
                'readonly': ~Eval('active', True),
                },
            depends=['active'],
            )
    iibb_number = fields.Char('II BB',
            states={
                'readonly': ~Eval('active', True),
                'required': And(Not(Equal(Eval('iibb_type'), 'exento')), Bool(Eval('iibb_type')))
                },
            depends=['active'],
            )
